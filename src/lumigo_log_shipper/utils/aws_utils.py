import gzip
import json
import base64
import os

import dacite

from lumigo_log_shipper.models import AwsLogSubscriptionEvent


def extract_aws_logs_data(event: dict) -> AwsLogSubscriptionEvent:
    logs_data_decoded = base64.b64decode(event["awslogs"]["data"])
    logs_data_unzipped = gzip.decompress(logs_data_decoded)
    logs_data_dict = json.loads(logs_data_unzipped)
    return dacite.from_dict(AwsLogSubscriptionEvent, logs_data_dict)


def extract_aws_logs_data_from_log_record(
    logs_data_dict: dict,
) -> AwsLogSubscriptionEvent:
    return dacite.from_dict(AwsLogSubscriptionEvent, logs_data_dict)


def get_current_region() -> str:
    return os.environ.get("AWS_REGION", "us-west-2")
