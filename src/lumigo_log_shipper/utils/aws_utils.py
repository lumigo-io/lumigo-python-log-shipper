import gzip
import json
import base64
import os
from typing import Optional

import dacite

from lumigo_log_shipper.models import AwsLogSubscriptionEvent


def extract_aws_logs_data(event: dict) -> AwsLogSubscriptionEvent:
    logs_data_decoded = base64.b64decode(event["awslogs"]["data"])
    logs_data_unzipped = gzip.decompress(logs_data_decoded)
    logs_data_dict = json.loads(logs_data_unzipped)
    logs_data_dict["region"] = get_current_region()
    return dacite.from_dict(AwsLogSubscriptionEvent, logs_data_dict)


def am_i_in_china() -> bool:
    return get_current_region() == "cn-northwest-1"


def get_current_region() -> Optional[str]:
    return os.environ.get("AWS_REGION")


def get_dest_region() -> str:
    if am_i_in_china():
        return "us-west-2"
    return get_current_region() or "us-west-2"
