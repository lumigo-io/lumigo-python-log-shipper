from dataclasses import asdict
from typing import List, Dict

from lumigo_log_shipper.models import AwsLogSubscriptionEvent, ShipperOutput
from lumigo_log_shipper.utils.consts import (
    STREAM_NAME,
    LOG_STREAM_KIIL_SWITCH,
    TARGET_ACCOUNT_ID,
    ENV,
    FILTER_KEYWORDS,
)
from lumigo_log_shipper.utils.firehose_dal import FirehoseDal
from lumigo_log_shipper.utils.aws_utils import (
    extract_aws_logs_data,
    extract_aws_logs_data_from_log_record,
)
from lumigo_log_shipper.utils.model_builder import parse_aws_extracted_data
from lumigo_log_shipper.utils.shipper_utils import should_report_log, filter_logs


def ship_logs(aws_event: dict, programtic_error_keyword: str = None) -> int:
    try:
        extracted_data: AwsLogSubscriptionEvent = extract_aws_logs_data(aws_event)
        shipper_output = parse_aws_extracted_data(extracted_data)
        return _ship_logs_to_lumigo(
            shipper_output=shipper_output,
            programtic_error_keyword=programtic_error_keyword,
        )
    except Exception:
        # lumigo_shipper dont raises Exceptions
        pass
    return 0


def _ship_aws_logs(aws_logs: List[Dict], programtic_error_keyword: str = None) -> int:
    try:
        shipper_output = []
        for aws_log in aws_logs:
            extracted_data: AwsLogSubscriptionEvent = extract_aws_logs_data_from_log_record(
                aws_log
            )
            shipper_output.extend(parse_aws_extracted_data(extracted_data))
        return _ship_logs_to_lumigo(
            shipper_output=shipper_output,
            programtic_error_keyword=programtic_error_keyword,
        )
    except Exception:
        # lumigo_shipper dont raises Exceptions
        pass
    return 0


def _ship_logs_to_lumigo(
    shipper_output: List[ShipperOutput], programtic_error_keyword: str = None
) -> int:
    filter_keywords = FILTER_KEYWORDS.copy()
    if programtic_error_keyword:
        filter_keywords.append(programtic_error_keyword)
    shipper_output = filter_logs(shipper_output, filter_keywords)
    if len(shipper_output) > 0 and not LOG_STREAM_KIIL_SWITCH:
        account_id = shipper_output[0].event_details.aws_account_id
        func_arn = shipper_output[0].event_details.function_details.resource_id
        if should_report_log(func_arn, account_id, TARGET_ACCOUNT_ID, ENV):
            firehose_records = list(map(asdict, shipper_output))
            firehose_dal = FirehoseDal(stream_name=STREAM_NAME, account_id=account_id)
            return firehose_dal.put_record_batch(firehose_records)
    return 0
