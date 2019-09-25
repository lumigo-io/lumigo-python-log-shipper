import gzip
import json
import base64
import os
from typing import Optional

from lumigo_log_shipper.models import AwsLogSubscriptionEvent, AwsLogEvent


def extract_aws_logs_data(event: dict) -> AwsLogSubscriptionEvent:
    logs_data_decoded = base64.b64decode(event["awslogs"]["data"])
    logs_data_unzipped = gzip.decompress(logs_data_decoded)
    logs_data_dict = json.loads(logs_data_unzipped)
    return AwsLogSubscriptionEvent(
        message_type=logs_data_dict.get("messageType"),
        owner=logs_data_dict.get("owner"),
        log_group=logs_data_dict.get("logGroup"),
        log_stream=logs_data_dict.get("logStream"),
        subscription_filters=logs_data_dict.get("subscriptionFilters"),
        log_events=[
            AwsLogEvent(
                id=event.get("id"),
                timestamp=event.get("timestamp"),
                message=event.get("message"),
            )
            for event in logs_data_dict.get("logEvents", [])
        ],
    )


def get_current_region() -> str:
    return os.environ.get("AWS_REGION", "us-west-2")


def get_function_name_from_arn(arn: str) -> str:
    return arn.split(":")[6]


def get_function_arn(extracted_data: AwsLogSubscriptionEvent) -> Optional[str]:
    region = get_current_region()
    if extracted_data.log_group:
        function_name = extracted_data.log_group.split("/")[3]
        return (
            f"arn:aws:lambda:{region}:{extracted_data.owner}:function:{function_name}"
        )
    return None
