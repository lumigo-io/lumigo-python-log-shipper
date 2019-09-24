from typing import List, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class AwsLogEvent:
    id: str
    timestamp: int
    message: str


@dataclass(frozen=True)
class AwsLogSubscriptionEvent:
    message_type: str
    owner: str
    log_group: str
    log_stream: str
    subscription_filters: List[str]
    log_events: List[AwsLogEvent]


@dataclass(frozen=True)
class FunctionDetails:
    resource_id: Optional[str]
    memory: float = 0.0  # We cant get memory of the running function from the log-shipper function


@dataclass(frozen=True)
class EventDetails:
    function_details: FunctionDetails
    aws_account_id: str
    timestamp: int


@dataclass(frozen=True)
class ShipperOutput:
    event_details: EventDetails
    timestamp: int
    message: str
