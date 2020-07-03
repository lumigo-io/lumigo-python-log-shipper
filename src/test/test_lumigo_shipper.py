import base64
import gzip
import json
from dataclasses import asdict

from lumigo_log_shipper.lumigo_shipper import ship_logs, _ship_aws_logs
from lumigo_log_shipper.models import AwsLogSubscriptionEvent, AwsLogEvent
from src.test.fixtures import *  # noqa


def test_lumigo_shipper_full_flow(simple_aws_event):
    records_send = ship_logs(simple_aws_event)
    assert records_send == 1


def test_lumigo_shipper_full_flow_with_programtic_error_keyword(simple_aws_event):
    records_send = ship_logs(simple_aws_event, "END")
    assert records_send == 1


def test_lumigo_aws_log_shipper_exception_not_throw_flow():
    records_send = _ship_aws_logs(None)
    assert records_send == 0


def test_lumigo_aws_log_shipper_exception_not_throw_flow_wrapper():
    records_send = ship_logs(None)
    assert records_send == 0


def test_lumigo_aws_log_shipper_full_flow():
    aws_log1 = {
        "messageType": "DATA_MESSAGE",
        "owner": "335722316285",
        "logGroup": "/aws/lambda/≈",
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

    aws_log2 = {
        "messageType": "DATA_MESSAGE",
        "owner": "335722316285",
        "logGroup": "/aws/lambda/group2",
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
    records_send = _ship_aws_logs([aws_log1, aws_log2])
    assert records_send == 2


def test_lumigo_aws_log_shipper_full_flow_with_programtic_error_keyword():
    aws_log1 = {
        "messageType": "DATA_MESSAGE",
        "owner": "335722316285",
        "logGroup": "/aws/lambda/≈",
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

    aws_log2 = {
        "messageType": "DATA_MESSAGE",
        "owner": "335722316285",
        "logGroup": "/aws/lambda/group2",
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
    records_send = _ship_aws_logs(
        aws_logs=[aws_log1, aws_log2], programmatic_error_keyword="END"
    )
    assert records_send == 2


def test_filter_logs_filter_filtering_invalid_items():
    raw_log = AwsLogSubscriptionEvent(
        messageType="DATA_MESSAGE",
        owner="335722316285",
        logGroup="/aws/lambda/test-http-req",
        logStream="2019/09/23/[$LATEST]041e7430c6d94506b2bc7b29bd021803",
        subscriptionFilters=["LambdaStream_random"],
        logEvents=[
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="NEW_FILTER RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="NEW_FILTER RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
        ],
    )

    records_send = ship_logs(
        _awsLogSubscriptionEvent_to_aws_event(raw_log), "NEW_FILTER"
    )

    assert records_send == 1


def test_filter_logs_filter_not_filtering_valid_items():
    raw_log = AwsLogSubscriptionEvent(
        messageType="DATA_MESSAGE",
        owner="335722316285",
        logGroup="/aws/lambda/test-http-req",
        logStream="2019/09/23/[$LATEST]041e7430c6d94506b2bc7b29bd021803",
        subscriptionFilters=["LambdaStream_random"],
        logEvents=[
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="SHOULD BE FILTERED",
            ),
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="SHOULD BE FILTERED",
            ),
        ],
    )

    records_send = ship_logs(_awsLogSubscriptionEvent_to_aws_event(raw_log), "END")

    assert records_send == 0


def _awsLogSubscriptionEvent_to_aws_event(event: AwsLogSubscriptionEvent) -> dict:
    logs_data = json.dumps(asdict(event))
    logs_data_zipped = gzip.compress(bytes(logs_data, "utf-8"))
    logs_data_encoded = base64.b64encode(logs_data_zipped)
    return {"awslogs": {"data": logs_data_encoded}}
