import boto3


def assume_role(target_account_id):
    client = boto3.client("sts")
    sts_response = client.assume_role(
        RoleArn=f"arn:aws:iam::{target_account_id}:role/CustomerLogsWriteRole",
        RoleSessionName="AssumeCrossAccountRole",
        DurationSeconds=900,
    )
    return sts_response
