import json
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Any
import boto3

from lumigo_log_shipper.utils.aws_utils import get_current_region
from lumigo_log_shipper.utils.consts import (
    TARGET_ACCOUNT_ID,
    SELF_ACCOUNT_ID,
    TARGET_ENV,
)
from lumigo_log_shipper.utils.encoder import DecimalEncoder
from lumigo_log_shipper.utils.log import get_logger
from lumigo_log_shipper.utils.sts import assume_role
from lumigo_log_shipper.utils.utils import split_to_chunks

MAX_RETRY_COUNT = 2
MAX_MESSAGES_TO_FIREHOSE = 500  # Firehose supports batch up to 500 messages.
MAX_FIREHOSE_RECORD_SIZE = 1024000
EOL = "\n"  # Firehose end of line mark
ENCODING = "utf-8"


@dataclass(frozen=True)
class Batch:
    records: List[Any]
    retry_count: int = 1


class FirehoseDal:
    def __init__(
        self,
        stream_name: str,
        account_id: str,
        max_retry_count: int = MAX_RETRY_COUNT,
        batch_size: int = MAX_MESSAGES_TO_FIREHOSE,
    ):
        """
        :param stream_name: Name of the firehose delivery stream.
        """
        self.current_account_id = account_id
        self._client = FirehoseDal.get_boto_client(account_id, TARGET_ACCOUNT_ID)
        self._stream_name = stream_name
        self.max_retry_count = max_retry_count
        self.failed_by_error_code: Dict[str, int] = defaultdict(int)
        self.batch_size = min(batch_size, MAX_MESSAGES_TO_FIREHOSE)
        get_logger().debug(
            f"Init firehose stream: {stream_name} target account: {TARGET_ACCOUNT_ID}"
        )

    def put_record_batch(self, records: List[dict]) -> int:
        """
        :param max_batch_size: max batch size
        :param records: The records to put
        :return: number of records inserted
        """
        number_of_records = 0
        firehose_records = self._convert_to_firehose_record(records)
        chunks = split_to_chunks(firehose_records, self.batch_size)
        batches: List[Batch] = self.create_batches_from_chunks(chunks)
        while batches:
            current_batch = batches.pop(0)
            should_retry = current_batch.retry_count < self.max_retry_count
            try:
                response = self._client.put_record_batch(
                    DeliveryStreamName=self._stream_name, Records=current_batch.records
                )["RequestResponses"]
                failed_items = self.get_failed_items(current_batch, response)
                self.update_failed_by_error_code(response)
                success_items_len = len(current_batch.records) - len(failed_items)
                number_of_records += success_items_len
                if any(failed_items) and should_retry:
                    batches.append(self.create_next_batch(current_batch, failed_items))
            except Exception as e:
                get_logger().debug(
                    "Error while trying to send data to firehose", exc_info=e,
                )
                self.failed_by_error_code[str(type(e).__name__)] += 1
                if should_retry:
                    next_records = current_batch.records
                    batches.append(self.create_next_batch(current_batch, next_records))
        return number_of_records

    def get_failed_items(
        self, current_batch: Batch, kinesis_response: List[dict]
    ) -> list:
        failed_items = []
        for index, response in enumerate(kinesis_response):
            if response.get("RecordId") is None:
                failed_items.append(current_batch.records[index])
        return failed_items

    def update_failed_by_error_code(self, kinesis_response: List[dict]) -> None:
        for response in kinesis_response:
            if response.get("RecordId") is None:
                error_code = response.get("ErrorCode")
                self.failed_by_error_code[str(error_code)] += 1

    @staticmethod
    def create_next_batch(current_batch: Batch, next_records: list) -> Batch:
        return Batch(records=next_records, retry_count=current_batch.retry_count + 1)

    @staticmethod
    def create_batches_from_chunks(chunks: List[list]) -> List[Batch]:
        return list(map(lambda b: Batch(records=b), chunks))

    @staticmethod
    def get_boto_client(account_id: str, target_account_id: str):
        region = get_current_region()
        if account_id != target_account_id and target_account_id != SELF_ACCOUNT_ID:
            sts_response = assume_role(target_account_id, TARGET_ENV)
            return boto3.client(
                "firehose",
                region_name=region,
                aws_access_key_id=sts_response["Credentials"]["AccessKeyId"],
                aws_secret_access_key=sts_response["Credentials"]["SecretAccessKey"],
                aws_session_token=sts_response["Credentials"]["SessionToken"],
            )
        return boto3.client("firehose")

    @staticmethod
    def _convert_to_firehose_record(records: List[dict]) -> List[dict]:
        fh_records: List[dict] = []
        for record in records:
            try:
                fh_record = json.dumps(record, cls=DecimalEncoder)
                if fh_record is not None:
                    fh_record += EOL
                    if len(fh_record) < MAX_FIREHOSE_RECORD_SIZE:
                        fh_records.append({"Data": fh_record})
            except Exception:
                # TODO: log error
                print("Failed to convert record to fh record")
        return fh_records
