import os

IS_LAMBDA_ENVIRONMENT = bool(os.environ.get("AWS_EXECUTION_ENV"))

MASTER_REGION = "us-west-2"

TARGET_ENV = os.environ.get("TARGET_ENV")
if TARGET_ENV == "" or TARGET_ENV is None:
    TARGET_ENV = "prod"

if TARGET_ENV == "SELF":
    TARGET_ENV = os.environ["ENV"] if IS_LAMBDA_ENVIRONMENT else os.environ["USER"]

STREAM_NAME = f"{TARGET_ENV}_logs-edge-stfl_customer-logs-firehose"

TARGET_ACCOUNT_ID = os.environ.get("TARGET_ACCOUNT_ID", "114300393969")
LOG_STREAM_KIIL_SWITCH = os.environ.get("LOG_STREAM_KIIL_SWITCH", None) == "TRUE"

SELF_ACCOUNT_ID = "SELF"

FILTER_KEYWORDS = [
    "Task timed out",
    "Process exited before completing request",
    "REPORT RequestId",
    "[ERROR]",
    "[LUMIGO_LOG]",
    "@lumigo",
    "LambdaRuntimeClientError",
    "Invoke Error",
    "Uncaught Exception",
    "Unhandled Promise Rejection",
]
