from dataclasses import asdict

from src.lumigo_log_shipper.models import AwsLogSubscriptionEvent
from src.lumigo_log_shipper.utils.consts import STREAM_NAME
from src.lumigo_log_shipper.utils.firehose_dal import FirehoseDal
from src.lumigo_log_shipper.utils.aws_utils import extract_aws_logs_data
from src.lumigo_log_shipper.utils.model_builder import parse_aws_extracted_data


def ship_logs(aws_event: dict) -> int:
    extracted_data: AwsLogSubscriptionEvent = extract_aws_logs_data(aws_event)
    shipper_output = parse_aws_extracted_data(extracted_data)
    firehose_records = list(map(asdict, shipper_output))
    firehose_dal = FirehoseDal(stream_name=STREAM_NAME)
    return firehose_dal.put_record_batch(firehose_records)
