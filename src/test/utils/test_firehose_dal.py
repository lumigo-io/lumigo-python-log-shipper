from collections import Counter
from typing import List

import pytest

from src.lumigo_log_shipper.utils.firehose_dal import FirehoseDal, Batch

RANDOM_RECORD_ID = "RANDOM_RECORD_ID"
RANDOM_ERROR_CODE = "RANDOM_ERROR_CODE"


def test_create_batched_from_chunks_simple():
    chunks = [[1], [2]]
    result = FirehoseDal.create_batched_from_chunks(chunks)
    assert result == [Batch([1], 1), Batch([2], 1)]


def test_create_next_batch():
    current_batch = Batch([1, 2], 1)
    next_items = [2]
    next_batch = FirehoseDal.create_next_batch(current_batch, next_items)

    assert next_batch == Batch([2], 2)


def test_get_failed_items_return_correct_items(
    kinesis_success_item, kinesis_failed_item
):
    current_batch = Batch(records=[1, 2])
    kinesis_response = [kinesis_success_item, kinesis_failed_item]
    firehose_service = FirehoseDal("random-stream-name")
    failed_items = firehose_service.get_failed_items(current_batch, kinesis_response)

    assert failed_items == [2]


def test_get_failed_items_add_to_failed_by_error_code(
    kinesis_success_item, kinesis_failed_item
):
    current_batch = Batch(records=[1, 2])
    kinesis_response = [kinesis_success_item, kinesis_failed_item]
    firehose_service = FirehoseDal("random-stream-name")
    firehose_service.get_failed_items(current_batch, kinesis_response)

    assert firehose_service.failed_by_error_code == Counter({RANDOM_ERROR_CODE: 1})


def test_put_records_happy_flow():
    firehose = FirehoseDal(stream_name="stream_name")
    assert firehose.put_record_batch(records=[{"id": 1}]) == 1


def test_put_records_happy_flow_with_non_default_max():
    firehose = FirehoseDal(stream_name="stream_name", batch_size=1)

    assert firehose.put_record_batch(records=[{"id": 1}]) == 1


def test_put_records_with_record_too_big():
    firehose = FirehoseDal(stream_name="stream_name")

    assert firehose.put_record_batch(records=[{"id": ("x" * 2048000)}]) == 0


def test_put_records_with_record_invalid():
    firehose = FirehoseDal(stream_name="stream_name")

    assert firehose.put_record_batch(records=[Exception()]) == 0  # noqa


def test_parse_firehose_from_record():
    firehose = FirehoseDal(stream_name="stream_name")
    firehose.put_record_batch(records=[{"id": 1}])


def test_put_records_error_on_first_try_success_in_second_try(monkeypatch):
    monkeypatch.setattr(
        FirehoseDal, "get_boto_client", lambda: MockFirehoseBotoClientRetryWithError()
    )
    firehose = FirehoseDal(stream_name="stream_name")

    assert firehose.put_record_batch(records=[{"id": 1}]) == 1


def test_put_records_exception_on_first_try_success_in_second_try(monkeypatch):
    client = MockFirehoseBotoClientException()
    monkeypatch.setattr(FirehoseDal, "get_boto_client", lambda: client)
    firehose = FirehoseDal(stream_name="stream_name")

    assert firehose.put_record_batch(records=[{"id": 1}]) == 1


def test_put_records_dont_retry_to_many_times(monkeypatch):
    monkeypatch.setattr(
        FirehoseDal, "get_boto_client", lambda: MockFirehoseBotoClientRetryWithError(3)
    )
    firehose = FirehoseDal(stream_name="stream_name", max_retry_count=2)

    assert firehose.put_record_batch(records=[{"id": 1}]) == 0


class MockFirehoseBotoClientRetryWithException:
    retry = 1

    def put_record_batch(self, DeliveryStreamName: str, Records: List[dict]):
        if self.retry > 0:
            self.retry = self.retry - 1
            raise Exception()
        return {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": "1"} for _ in Records],
        }


class MockFirehoseBotoClientRetryWithError:
    def __init__(self, retry=1):
        self.retry = retry

    def put_record_batch(self, DeliveryStreamName: str, Records: List[dict]):
        if self.retry > 0:
            self.retry = self.retry - 1
            return {
                "FailedPutCount": 0,
                "RequestResponses": [
                    {
                        "ErrorCode": "ServiceUnavailableException",
                        "ErrorMessage": "ServiceUnavailableException",
                    }
                    for _ in Records
                ],
            }
        return {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": "1"} for _ in Records],
        }


class MockFirehoseBotoClientException:
    retry = 1
    records: List = []

    def put_record_batch(self, DeliveryStreamName: str, Records: List[dict]):
        if self.retry > 0:
            self.retry = self.retry - 1
            raise Exception()
        self.records.extend(Records)
        return {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": "1"} for _ in Records],
        }


@pytest.fixture
def kinesis_success_item() -> dict:
    return {"RecordId": RANDOM_RECORD_ID}


@pytest.fixture
def kinesis_failed_item() -> dict:
    return {"ErrorCode": RANDOM_ERROR_CODE}
