from typing import List

from pytest import fixture

from lumigo_log_shipper.utils.firehose_dal import FirehoseDal


class MockFirehoseBotoClient:
    def put_record_batch(self, DeliveryStreamName: str, Records: List[dict]):
        return {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": "1"} for _ in Records],
        }


@fixture(autouse=True)
def firehose_dal_mock(monkeypatch):
    monkeypatch.setattr(
        FirehoseDal, "get_boto_client", lambda x, y: MockFirehoseBotoClient()
    )
    yield
