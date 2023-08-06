# Halloumi Cloudwatch Dashboard

Create a dashboard in the AWS Cloudwatch using the best practices from Halloumi.

## Install

From pip:

```bash
pip install halloumi-cloudwatch-dashboard
```

From npm:

```bash
npm install halloumi-cloudwatch-dashboard
```

## API Documentation

Check [API Documentation](./API.md)

## Usage

### Python

```python
from aws_cdk import core
from halloumi-cloudwatch-dashboard import Dashboard

app = core.App()

stack = core.Stack(app, 'MainStack')
...

Dashboard(
    stack,
    'Dashboard',
    dashboardName='MyDashboard'
)
```

### Typescript

```python
# Example automatically generated from non-compiling source. May contain errors.
import aws_cdk.core as cdk
from halloumi_cloudwatch_dashboard import Dashboard

class CdkWorkshopStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        Dashboard(self, "Dashboard", dashboard_name = "MyDashboard")
```
