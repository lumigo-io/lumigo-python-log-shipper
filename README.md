![CircleCI](https://circleci.com/gh/lumigo-io/lumigo-python-log-shipper/tree/master.svg?style=svg&circle-token=82bcda94717aed3dc5068e1643922ffc0ad039c6)
[![codecov](https://codecov.io/gh/lumigo-io/lumigo-python-log-shipper/branch/master/graph/badge.svg?token=jlGd29sam6)](https://codecov.io/gh/lumigo-io/lumigo-python-log-shipper)
![Version](https://badge.fury.io/py/lumigo-log-shipper.svg)
# lumigo-python-log-shipper

[`lumigo-log-shipper`](https://pypi.org/project/lumigo-log-shipper/) is Lumigo's log shipper for Python

## Usage 

Install `lumigo-log-shipper`:

pip: 
~~~bash
$ pip3 install lumigo-log-shipper
~~~

In your lambda's code: 
~~~python
from lumigo_log_shipper import lumigo_shipper

def handler(event, context):
    lumigo_shipper.ship_logs(event)
~~~

With programtic error:
~~~python
from lumigo_log_shipper import lumigo_shipper

def handler(event, context):
    lumigo_shipper.ship_logs(event, ["WARNING-EXAMPLE"])
~~~
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
        - "arn:aws:iam::114300393969:role/CustomerLogsWriteRole"
```
