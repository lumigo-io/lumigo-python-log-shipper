![CircleCI](https://circleci.com/gh/lumigo-io/lumigo-python-log-shipper/tree/master.svg?style=svg&circle-token=82bcda94717aed3dc5068e1643922ffc0ad039c6)
[![codecov](https://codecov.io/gh/lumigo-io/lumigo-python-log-shipper/branch/master/graph/badge.svg?token=jlGd29sam6)](https://codecov.io/gh/lumigo-io/lumigo-python-log-shipper)
![Version](https://badge.fury.io/py/lumigo-log-shipper.svg)

# lumigo-python-log-shipper

Lumigo Log Shipper API lets you stream your Lambda functions' logs to Lumigo as a part of your custom log shipping function.

NOTE: Lumigo will automatically try to subscribe your Lambda functions to a Kinesis data stream. In case your log group is already subscribed to a Lambda as a destination, use this library to send logs to Lumigo.

Please contact Lumigo's support through the platform chat so we can enable this feature for you.

## Usage

Install `lumigo-log-shipper`:

pip:

```bash
> pip install lumigo-log-shipper
```

In your log shipping Lambda's code:

```python
from lumigo_log_shipper import lumigo_shipper

def handler(event, context):
    lumigo_shipper.ship_logs(event)
```

If you are using programmatic errors, add your custom error keyword as an additional parameter.
This will also send logs which contains your custom expression for Lumigo to process.

```python
from lumigo_log_shipper import lumigo_shipper

def handler(event, context):
    lumigo_shipper.ship_logs(event, ["WARNING-EXAMPLE"])
```

Add to your lambda's `serverless.yml`

```bash
  iamRoleStatements:
    - Effect: Allow
      Action:
        - "firehose:PutRecordBatch"
      Resource:
        - "arn:aws:firehose:[YOUR-REGION]:114300393969:deliverystream/prod_logs-edge-stfl_customer-logs-firehose"
    - Effect: Allow
      Action:
        - "sts:AssumeRole"
      Resource:
        - "arn:aws:iam::114300393969:role/prod-CustomerLogsWriteRole"
```
