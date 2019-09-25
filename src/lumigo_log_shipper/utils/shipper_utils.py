from typing import Optional, List

from lumigo_log_shipper.models import ShipperOutput
from lumigo_log_shipper.utils.aws_utils import get_function_name_from_arn
from lumigo_log_shipper.utils.consts import SELF_ACCOUNT_ID


def should_report_log(
    function_arn: Optional[str], account_id: str, target_account_id: str, env: str
):
    """
    Protection for streaming logs, we dont send logs of our backend to the same account
    """
    if function_arn:
        func_name = get_function_name_from_arn(function_arn)
        is_sending_to_self = (
            account_id == target_account_id or target_account_id == SELF_ACCOUNT_ID
        )
        is_func_in_my_env = func_name.startswith(env)
        if not is_sending_to_self or not is_func_in_my_env:
            return True
    return False


def _is_valid_log(log_message: str, filter_keywords: List[str]):
    for keyword in filter_keywords:
        if keyword.lower() in log_message.lower():
            return True
    return False


def filter_logs(
    logs: List[ShipperOutput], filter_keywords: List[str]
) -> List[ShipperOutput]:
    return [log for log in logs if _is_valid_log(log.message, filter_keywords)]
