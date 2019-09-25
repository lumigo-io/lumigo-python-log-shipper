from typing import Optional

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
        send_to_myself = (
            account_id == target_account_id or target_account_id == SELF_ACCOUNT_ID
        )
        if not send_to_myself or not func_name.startswith(env):
            return True
    return False
