import pytest

from lumigo_log_shipper.models import AwsLogSubscriptionEvent, AwsLogEvent
from lumigo_log_shipper.utils.aws_utils import (
    extract_aws_logs_data,
    is_china_region,
    get_dest_region,
)
from src.test.fixtures import *  # noqa


def test_extract_aws_logs_data_simple_flow(simple_aws_event):
    result = extract_aws_logs_data(simple_aws_event)

    assert result == AwsLogSubscriptionEvent(
        messageType="DATA_MESSAGE",
        owner="335722316285",
        logGroup="/aws/lambda/test-http-req",
        logStream="2019/09/23/[$LATEST]041e7430c6d94506b2bc7b29bd021803",
        subscriptionFilters=["LambdaStream_random"],
        logEvents=[
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488768",
                timestamp=1_569_238_311_100,
                message="END RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\n",
            ),
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1_569_238_311_100,
                message="REPORT RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
        ],
        region="us-west-2",
    )


def test_is_china_region_not_china():
    assert is_china_region() is False


def test_is_china_region_in_china(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "cn-northwest-1")
    assert is_china_region() is True


@pytest.mark.parametrize(
    ["current_region", "expected_region"],
    [["us-east-1", "us-east-1"], ["cn-northwest-1", "us-west-2"]],
)
def test_get_dest_region(monkeypatch, current_region, expected_region):
    monkeypatch.setenv("AWS_REGION", current_region)
    assert get_dest_region() == expected_region
