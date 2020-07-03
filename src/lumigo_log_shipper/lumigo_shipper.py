from dataclasses import asdict
from typing import List, Dict, Optional

from lumigo_log_shipper.models import AwsLogSubscriptionEvent
from lumigo_log_shipper.utils.consts import (
    STREAM_NAME,
    LOG_STREAM_KIIL_SWITCH,
    FILTER_KEYWORDS,
)
from lumigo_log_shipper.utils.firehose_dal import FirehoseDal
from lumigo_log_shipper.utils.aws_utils import (
    extract_aws_logs_data,
    extract_aws_logs_data_from_log_record,
)
from lumigo_log_shipper.utils.log import get_logger
from lumigo_log_shipper.utils.shipper_utils import filter_logs


def ship_logs(aws_event: dict, programmatic_error_keyword: str = None) -> int:
    try:
        shipper_output: AwsLogSubscriptionEvent = extract_aws_logs_data(aws_event)
        res = _ship_logs_to_lumigo(
            shipper_outputs=[shipper_output],
            programmatic_error_keyword=programmatic_error_keyword,
        )
        get_logger().info(f"Successfully sent {res} logs")
        return res
    except Exception as e:
        # lumigo_shipper will print out the exception but won't raises it
        get_logger().critical("Failed to send customer logs", exc_info=e)
    return 0


def _ship_aws_logs(aws_logs: List[Dict], programmatic_error_keyword: str = None) -> int:
    try:
        shipper_outputs: List[AwsLogSubscriptionEvent] = []
        for aws_log in aws_logs:
            extracted_data: AwsLogSubscriptionEvent = extract_aws_logs_data_from_log_record(
                aws_log
            )
            shipper_outputs.append(extracted_data)
        return _ship_logs_to_lumigo(
            shipper_outputs=shipper_outputs,
            programmatic_error_keyword=programmatic_error_keyword,
        )
    except Exception:
        # lumigo_shipper dont raises Exceptions
        pass
    return 0


def _ship_logs_to_lumigo(
    shipper_outputs: List[AwsLogSubscriptionEvent],
    programmatic_error_keyword: Optional[str] = None,
) -> int:
    get_logger().debug(f"Number of logs before filter {len(shipper_outputs)}")
    filter_keywords = FILTER_KEYWORDS.copy()
    if programmatic_error_keyword:
        filter_keywords.append(programmatic_error_keyword)
    shipper_outputs = filter_logs(shipper_outputs, filter_keywords)
    get_logger().debug(f"Number of logs after filter {len(shipper_outputs)}")
    if len(shipper_outputs) > 0 and not LOG_STREAM_KIIL_SWITCH:
        account_id = shipper_outputs[0].owner
        firehose_records = list(map(asdict, shipper_outputs))
        firehose_dal = FirehoseDal(stream_name=STREAM_NAME, account_id=account_id)
        return firehose_dal.put_record_batch(firehose_records)
    return 0
