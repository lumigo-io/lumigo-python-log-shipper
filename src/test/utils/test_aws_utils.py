from lumigo_log_shipper.models import AwsLogSubscriptionEvent, AwsLogEvent
from lumigo_log_shipper.utils.aws_utils import (
    extract_aws_logs_data,
    extract_aws_logs_data_from_log_record,
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
    )


def test_extract_aws_logs_data_from_log_record_simple_flow():
    aws_log = {
        "messageType": "DATA_MESSAGE",
        "owner": "335722316285",
        "logGroup": "/aws/lambda/test-http-req",
        "logStream": "2019/09/23/[$LATEST]041e7430c6d94506b2bc7b29bd021803",
        "subscriptionFilters": ["LambdaStream_random"],
        "logEvents": [
            {
                "id": "34995183731613629262151179513935230756777419834003488768",
                "timestamp": 1569238311100,
                "message": "END RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\n",
            },
            {
                "id": "34995183731613629262151179513935230756777419834003488769",
                "timestamp": 1569238311100,
                "message": "REPORT RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            },
        ],
    }
    result = extract_aws_logs_data_from_log_record(aws_log)

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
    )
