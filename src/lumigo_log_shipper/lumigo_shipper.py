from dataclasses import asdict
from typing import List, Optional

from lumigo_log_shipper.models import AwsLogSubscriptionEvent
from lumigo_log_shipper.utils.consts import (
    STREAM_NAME,
    LOG_STREAM_KIIL_SWITCH,
    FILTER_KEYWORDS,
)
from lumigo_log_shipper.utils.firehose_dal import FirehoseDal
from lumigo_log_shipper.utils.aws_utils import extract_aws_logs_data
from lumigo_log_shipper.utils.log import get_logger
from lumigo_log_shipper.utils.shipper_utils import filter_logs
from lumigo_log_shipper.utils.sts import ChinaMissingEnvVar


def ship_logs(
    aws_event: dict,
    programmatic_error_keyword: Optional[str] = None,
    exclude_filters: Optional[List[str]] = None,
) -> int:
    try:
        shipper_output: AwsLogSubscriptionEvent = extract_aws_logs_data(aws_event)
        res = _ship_logs_to_lumigo(
            shipper_outputs=[shipper_output],
            programmatic_error_keyword=programmatic_error_keyword,
            exclude_filters=exclude_filters,
        )
        get_logger().info(f"Successfully sent {res} logs")
        return res
    except ChinaMissingEnvVar:
        pass
    except Exception as e:
        # lumigo_shipper will print out the exception but won't raises it
        get_logger().critical("Failed to send customer logs", exc_info=e)
    return 0


def _ship_logs_to_lumigo(
    shipper_outputs: List[AwsLogSubscriptionEvent],
    programmatic_error_keyword: Optional[str] = None,
    exclude_filters: Optional[List[str]] = None,
) -> int:
    get_logger().debug(f"Number of logs before filter {len(shipper_outputs)}")
    filter_keywords = FILTER_KEYWORDS.copy()
    if programmatic_error_keyword:
        filter_keywords.append(programmatic_error_keyword)
    shipper_outputs = filter_logs(shipper_outputs, filter_keywords, exclude_filters)
    get_logger().debug(f"Number of logs after filter {len(shipper_outputs)}")
    if len(shipper_outputs) > 0 and not LOG_STREAM_KIIL_SWITCH:
        account_id = shipper_outputs[0].owner
        firehose_records = list(map(asdict, shipper_outputs))
        firehose_dal = FirehoseDal(stream_name=STREAM_NAME, account_id=account_id)
        return firehose_dal.put_record_batch(firehose_records)
    return 0
