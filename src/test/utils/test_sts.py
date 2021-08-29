from unittest.mock import MagicMock

import boto3
from moto import mock_sts
import pytest

from lumigo_log_shipper.utils.sts import assume_role, ChinaMissingEnvVar


def test_assume_role_china_missing_access_key(monkeypatch, caplog):
    monkeypatch.setenv("AWS_REGION", "cn-northwest-1")
    with pytest.raises(ChinaMissingEnvVar):
        assume_role("111111111111", "unitteset")
    assert "CRITICAL" in caplog.text
    assert "LUMIGO_LOGS_EDGE_AWS_ACCESS_KEY_ID" in caplog.text


def test_assume_role_china_missing_secret_key(monkeypatch, caplog):
    monkeypatch.setenv("LUMIGO_LOGS_EDGE_AWS_ACCESS_KEY_ID", "111")
    monkeypatch.setenv("AWS_REGION", "cn-northwest-1")
    with pytest.raises(ChinaMissingEnvVar):
        assume_role("111111111111", "unitteset")
    assert "CRITICAL" in caplog.text
    assert "LUMIGO_LOGS_EDGE_AWS_SECRET_ACCESS_KEY" in caplog.text


@mock_sts
def test_assume_role(monkeypatch):
    original_client = boto3.client
    mocked_client = MagicMock(side_effect=original_client)
    monkeypatch.setattr(boto3, "client", mocked_client)

    assume_role("111111111111", "unitteset")

    mocked_client.assert_called_with("sts")


@mock_sts
def test_assume_role_china(monkeypatch):
    monkeypatch.setenv("LUMIGO_LOGS_EDGE_AWS_ACCESS_KEY_ID", "key1")
    monkeypatch.setenv("LUMIGO_LOGS_EDGE_AWS_SECRET_ACCESS_KEY", "secret1")
    monkeypatch.setenv("AWS_REGION", "cn-northwest-1")
    original_client = boto3.client
    mocked_client = MagicMock(side_effect=original_client)
    monkeypatch.setattr(boto3, "client", mocked_client)

    assume_role("111111111111", "unitteset")

    mocked_client.assert_called_with(
        "sts",
        region_name="us-west-2",
        aws_access_key_id="key1",
        aws_secret_access_key="secret1",
    )
