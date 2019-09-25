from lumigo_log_shipper.lumigo_shipper import ship_logs
from lumigo_log_shipper.models import AwsLogSubscriptionEvent, AwsLogEvent
from lumigo_log_shipper.utils.model_builder import parse_aws_extracted_data
from lumigo_log_shipper.utils.shipper_utils import should_report_log, filter_logs
from src.test.fixtures import *  # noqa


def test_lumigo_shipper_full_flow(simple_aws_event):
    records_send = ship_logs(simple_aws_event)
    assert records_send == 1


def test_should_report_same_env_other_target():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "22", "d") is True


def test_should_report_same_env_same_target_by_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "11", "d") is False


def test_should_report_same_env_same_target_by_self_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "SELF", "d") is False


def test_should_report_other_env_same_target_by_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "11", "e") is True


def test_should_report_other_env_same_target_by_self_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "SELF", "e") is True


def test_filter_logs_filter_not_filtering_invalid_items():
    raw_logs = AwsLogSubscriptionEvent(
        message_type="DATA_MESSAGE",
        owner="335722316285",
        log_group="/aws/lambda/test-http-req",
        log_stream="2019/09/23/[$LATEST]041e7430c6d94506b2bc7b29bd021803",
        subscription_filters=["LambdaStream_random"],
        log_events=[
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="END RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="END RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
        ],
    )
    shipper_output = parse_aws_extracted_data(raw_logs)
    result = filter_logs(shipper_output, ["report"])
    assert result == []


def test_filter_logs_filter_not_filtering_valid_items():
    raw_logs = AwsLogSubscriptionEvent(
        message_type="DATA_MESSAGE",
        owner="335722316285",
        log_group="/aws/lambda/test-http-req",
        log_stream="2019/09/23/[$LATEST]041e7430c6d94506b2bc7b29bd021803",
        subscription_filters=["LambdaStream_random"],
        log_events=[
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="REPORT RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
            AwsLogEvent(
                id="34995183731613629262151179513935230756777419834003488769",
                timestamp=1569238311100,
                message="REPORT RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
            ),
        ],
    )
    shipper_output = parse_aws_extracted_data(raw_logs)
    result = filter_logs(shipper_output, ["report"])
    assert result == shipper_output
