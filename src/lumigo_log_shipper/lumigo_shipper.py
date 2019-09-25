from dataclasses import asdict

from lumigo_log_shipper.models import AwsLogSubscriptionEvent
from lumigo_log_shipper.utils.consts import (
    STREAM_NAME,
    LOG_STREAM_KIIL_SWITCH,
    TARGET_ACCOUNT_ID,
    ENV,
)
from lumigo_log_shipper.utils.firehose_dal import FirehoseDal
from lumigo_log_shipper.utils.aws_utils import extract_aws_logs_data
from lumigo_log_shipper.utils.model_builder import parse_aws_extracted_data
from lumigo_log_shipper.utils.shipper_utils import should_report_log


def ship_logs(aws_event: dict) -> int:
    extracted_data: AwsLogSubscriptionEvent = extract_aws_logs_data(aws_event)
    shipper_output = parse_aws_extracted_data(extracted_data)
    if len(shipper_output) > 0 and not LOG_STREAM_KIIL_SWITCH:
        account_id = shipper_output[0].event_details.aws_account_id
        func_arn = shipper_output[0].event_details.function_details.resource_id
        if should_report_log(func_arn, account_id, TARGET_ACCOUNT_ID, ENV):
            firehose_records = list(map(asdict, shipper_output))
            firehose_dal = FirehoseDal(stream_name=STREAM_NAME, account_id=account_id)
            return firehose_dal.put_record_batch(firehose_records)
    return 0
