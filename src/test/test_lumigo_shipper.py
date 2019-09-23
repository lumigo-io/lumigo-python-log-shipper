from src.lumigo_log_shipper.lumigo_shipper import LumigoShipper
from src.test.fixtures import *


def test_lumigo_shipper_full_flow(simple_aws_event):
    shipper = LumigoShipper()
    records_send = shipper.ship_logs(simple_aws_event)
    assert records_send == 2
