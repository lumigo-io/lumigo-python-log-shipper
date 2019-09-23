from src.utils.firehose_dal import FirehoseDal

STREAM_NAME = "logs-edge-stfl_customer-logs-firehose"


# TODO: Get current region
def ship_logs(logs, region="us-west-2", env="doriaviram", account_id="335722316285"):
    try:
        stream_name = (
            f"arn:aws:firehose:{region}:{account_id}:deliverystream/{env}_{STREAM_NAME}"
        )
        kinesis = FirehoseDal(stream_name=stream_name)
        kinesis.put_record_batch(logs)
    except Exception as e:
        # TODO: Handle
        print(e)
