from typing import List

from lumigo_log_shipper.models import (
    AwsLogSubscriptionEvent,
    ShipperOutput,
    EventDetails,
    FunctionDetails,
)
from lumigo_log_shipper.utils.aws_utils import get_function_arn


def parse_aws_extracted_data(
    extracted_data: AwsLogSubscriptionEvent
) -> List[ShipperOutput]:
    result: List[ShipperOutput] = []
    function_arn = get_function_arn(extracted_data)
    for log_event in extracted_data.log_events:
        shipper_output = ShipperOutput(
            message=log_event.message,
            timestamp=log_event.timestamp,
            event_details=EventDetails(
                aws_account_id=extracted_data.owner,
                timestamp=log_event.timestamp,
                function_details=FunctionDetails(resource_id=function_arn),
            ),
        )
        result.append(shipper_output)
    return result
