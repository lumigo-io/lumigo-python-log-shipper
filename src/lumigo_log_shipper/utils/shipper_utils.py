from typing import List, Optional

from lumigo_log_shipper.models import AwsLogSubscriptionEvent


def _is_valid_log(
    log_message: str,
    filter_keywords: List[str],
    exclude_filters: Optional[List[str]] = None,
):
    log_message = str(log_message)
    log_message_lower = log_message.lower()
    if exclude_filters:
        for exclude_filter in exclude_filters:
            if exclude_filter.lower() in log_message_lower:
                return False
    for keyword in filter_keywords:
        if keyword.lower() in log_message_lower:
            return True
    return False


def filter_logs(
    logs: List[AwsLogSubscriptionEvent],
    filter_keywords: List[str],
    exclude_filters: Optional[List[str]] = None,
) -> List[AwsLogSubscriptionEvent]:
    res_list: List[AwsLogSubscriptionEvent] = []
    for log in logs:
        filtered_events = list(
            filter(
                lambda event: _is_valid_log(
                    event.message, filter_keywords, exclude_filters
                ),
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
                    region=log.region,
                )
            )

    return res_list
