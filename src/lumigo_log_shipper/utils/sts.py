import boto3


def assume_role(target_account_id, target_env):
    client = boto3.client("sts")
    sts_response = client.assume_role(
        RoleArn=f"arn:aws:iam::{target_account_id}:role/{target_env}-CustomerLogsWriteRole",
        RoleSessionName="AssumeCrossAccountRole",
        DurationSeconds=900,
    )
    return sts_response
