from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class AwsLogEvent:
    id: str
    timestamp: int
    message: str


@dataclass(frozen=True)
class AwsLogSubscriptionEvent:
    messageType: str
    owner: str
    logGroup: str
    logStream: str
    subscriptionFilters: List[str]
    logEvents: List[AwsLogEvent]
