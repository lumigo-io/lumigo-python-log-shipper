from typing import List

from pytest import fixture, yield_fixture

from src.lumigo_log_shipper.utils.firehose_dal import FirehoseDal


def mock_boto_firehose_client():
    return MockFirehoseBotoClient()


class MockFirehoseBotoClient:
    def put_record_batch(self, DeliveryStreamName: str, Records: List[dict]):
        return {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": "1"} for _ in Records],
        }


@yield_fixture
def firehose_dal(monkeypatch) -> FirehoseDal:
    monkeypatch.setattr(FirehoseDal, "get_boto_client", mock_boto_firehose_client)
    yield


@fixture(autouse=True)
def firehose_dal_mock(firehose_dal):
    pass
