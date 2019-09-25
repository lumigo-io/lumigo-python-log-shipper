from lumigo_log_shipper.lumigo_shipper import ship_logs
from lumigo_log_shipper.utils.shipper_utils import should_report_log
from src.test.fixtures import *  # noqa


def test_lumigo_shipper_full_flow(simple_aws_event):
    records_send = ship_logs(simple_aws_event)
    assert records_send == 2


def test_should_report_same_env_other_target():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "22", "d") is True


def test_should_report_same_env_same_target_by_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "11", "d") is False


def test_should_report_same_env_same_target_by_self_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "SELF", "d") is False


def test_should_report_other_env_same_target_by_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "11", "e") is True


def test_should_report_other_env_same_target_by_self_account_id():
    arn = "arn:aws:lambda:us-west-2:11:function:d_func_name"
    assert should_report_log(arn, "11", "SELF", "e") is True
