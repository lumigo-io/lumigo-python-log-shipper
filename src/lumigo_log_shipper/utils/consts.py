import os

IS_LAMBDA_ENVIRONMENT = (
    True if ("AWS_EXECUTION_ENV" in os.environ and os.environ["AWS_EXECUTION_ENV"]) else False
)

MASTER_REGION = "us-west-2"

ENV = os.environ["ENV"] if IS_LAMBDA_ENVIRONMENT else os.environ["USER"]

STREAM_NAME = f"{ENV}_logs-edge-stfl_customer-logs-firehose"