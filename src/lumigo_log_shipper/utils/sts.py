import boto3
import os

from lumigo_log_shipper.utils.aws_utils import is_china_region
from lumigo_log_shipper.utils.log import get_logger


def _get_china_env_var(env_var_name: str) -> str:
    value = os.environ.get(env_var_name)
    if value:
        return value
    get_logger().critical(
        f"Failed to send customer logs because {env_var_name} env var is missing and it is needed in China"
    )
    raise ChinaMissingEnvVar()


def _get_boto_sts_client():
    if not is_china_region():
        return boto3.client("sts")
    aws_access_key_id = _get_china_env_var("LUMIGO_LOGS_EDGE_AWS_ACCESS_KEY_ID")
    aws_secret_access_key = _get_china_env_var("LUMIGO_LOGS_EDGE_AWS_SECRET_ACCESS_KEY")
    return boto3.client(
        "sts",
        region_name=os.environ.get("LUMIGO_LOGS_EDGE_REGION", "us-west-2"),
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


def assume_role(target_account_id, target_env):
    client = _get_boto_sts_client()
    sts_response = client.assume_role(
        RoleArn=f"arn:aws:iam::{target_account_id}:role/{target_env}-CustomerLogsWriteRole",
        RoleSessionName="AssumeCrossAccountRole",
        DurationSeconds=900,
    )
    return sts_response


class ChinaMissingEnvVar(Exception):
    pass
