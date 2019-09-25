# lumigo-python-log-shipper
```
from lumigo_log_shipper import lumigo_shipper
def my_lambda(event, context):
    lumigo_shipper.ship_logs(event)
```

With programtic error:
```
from lumigo_log_shipper import lumigo_shipper
def my_lambda(event, context):
    lumigo_shipper.ship_logs(event, "[Error]")
```
