from typing import List

from lumigo_log_shipper.models import AwsLogSubscriptionEvent


def _is_valid_log(log_message: str, filter_keywords: List[str]):
    log_message = str(log_message)
    for keyword in filter_keywords:
        if keyword.lower() in log_message.lower():
            return True
    return False


def filter_logs(
    logs: List[AwsLogSubscriptionEvent], filter_keywords: List[str]
) -> List[AwsLogSubscriptionEvent]:
    res_list: List[AwsLogSubscriptionEvent] = []
    for log in logs:
        filtered_events = list(
            filter(
                lambda event: _is_valid_log(event.message, filter_keywords),
                log.logEvents,
            )
        )
        if len(filtered_events) > 0:
            res_list.append(
                AwsLogSubscriptionEvent(
                    messageType=log.messageType,
                    owner=log.owner,
                    logGroup=log.logGroup,
                    logStream=log.logStream,
                    subscriptionFilters=log.subscriptionFilters,
                    logEvents=filtered_events,
                )
            )

    return res_list
