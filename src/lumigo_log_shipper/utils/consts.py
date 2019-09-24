import os

IS_LAMBDA_ENVIRONMENT = bool(os.environ.get("AWS_EXECUTION_ENV"))

MASTER_REGION = "us-west-2"

ENV = os.environ["ENV"] if IS_LAMBDA_ENVIRONMENT else os.environ["USER"]

STREAM_NAME = f"{ENV}_logs-edge-stfl_customer-logs-firehose"
