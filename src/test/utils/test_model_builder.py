from lumigo_log_shipper.models import ShipperOutput, EventDetails, FunctionDetails
from lumigo_log_shipper.utils.model_builder import parse_aws_extracted_data
from src.test.fixtures import *  # noqa


def test_parse_aws_extracted_data_simple_flow(simple_extracted_data):
    shipper_output = parse_aws_extracted_data(simple_extracted_data)
    assert shipper_output == [
        ShipperOutput(
            event_details=EventDetails(
                function_details=FunctionDetails(
                    resource_id="arn:aws:lambda:us-west-2:335722316285:function:test-http-req",
                    memory=0,
                ),
                aws_account_id="335722316285",
                timestamp=1569238311100,
            ),
            timestamp=1569238311100,
            message="END RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\n",
        ),
        ShipperOutput(
            event_details=EventDetails(
                function_details=FunctionDetails(
                    resource_id="arn:aws:lambda:us-west-2:335722316285:function:test-http-req",
                    memory=0,
                ),
                aws_account_id="335722316285",
                timestamp=1569238311100,
            ),
            timestamp=1569238311100,
            message="REPORT RequestId: 972f23e6-efab-4897-80a0-12b8f8a28190\tDuration: 100.00 ms\tBilled Duration: 200 ms\tMemory Size: 128 MB\tMax Memory Used: 75 MB\tInit Duration: 156.08 ms\t\nXRAY TraceId: 1-5d88ad26-af7e1cf86161c0887567eed0\tSegmentId: 2ea934c013374041\tSampled: false\t\n",
        ),
    ]
