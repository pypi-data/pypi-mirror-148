'''
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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_autoscaling
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_elasticache
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_rds
import aws_cdk.core


class Dashboard(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-cloudwatch-dashboard.Dashboard",
):
    '''An AWS CloudWatch Dashboard.

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        # create a dashboard for AutoScaling
        Dashboard(self, "dashboard",
            auto_scaling_name="my-auto-scaling",
            auto_scaling_max_capacity=10
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_scaling: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_autoscaling.AutoScalingGroup, aws_cdk.aws_autoscaling.CfnAutoScalingGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, typing.Sequence[jsii.Number]]]]]] = None,
        elasticache: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_elasticache.CfnReplicationGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]]]] = None,
        load_balancer: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer, aws_cdk.aws_elasticloadbalancingv2.CfnLoadBalancer, typing.Mapping[builtins.str, builtins.str]]]] = None,
        rds: typing.Optional[typing.Sequence[aws_cdk.aws_rds.CfnDBCluster]] = None,
        dashboard_name: typing.Optional[builtins.str] = None,
        end: typing.Optional[builtins.str] = None,
        period_override: typing.Optional[aws_cdk.aws_cloudwatch.PeriodOverride] = None,
        start: typing.Optional[builtins.str] = None,
        widgets: typing.Optional[typing.Sequence[typing.Sequence[aws_cdk.aws_cloudwatch.IWidget]]] = None,
    ) -> None:
        '''Creates a Dashboard based on the Halloumi best practices.

        :param scope: the scope into which to import this dashboard.
        :param id: the logical ID of the returned dashboard construct.
        :param auto_scaling: List of AutoScaling. If set, must only contain a list of AutoScaling or Dictionary "{ 'name': string, 'max_capacity': number }" Default: - None
        :param elasticache: List of Elasticache. If set, must only contain a list of Elasticache or Dictionary "{ 'name': string, 'nodes': number }" with nodes being optional Default: - None
        :param load_balancer: List of LoadBalancers. If set, must only contain a list of LoadBalancer or Dictionary "{ 'name': string, 'full_name': string }" Default: - None
        :param rds: List of RDS. If set, must only contain a list of RDS Default: - None
        :param dashboard_name: Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets
        '''
        props = HalloumiDashboard(
            auto_scaling=auto_scaling,
            elasticache=elasticache,
            load_balancer=load_balancer,
            rds=rds,
            dashboard_name=dashboard_name,
            end=end,
            period_override=period_override,
            start=start,
            widgets=widgets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="halloumi-cloudwatch-dashboard.HalloumiDashboard",
    jsii_struct_bases=[aws_cdk.aws_cloudwatch.DashboardProps],
    name_mapping={
        "dashboard_name": "dashboardName",
        "end": "end",
        "period_override": "periodOverride",
        "start": "start",
        "widgets": "widgets",
        "auto_scaling": "autoScaling",
        "elasticache": "elasticache",
        "load_balancer": "loadBalancer",
        "rds": "rds",
    },
)
class HalloumiDashboard(aws_cdk.aws_cloudwatch.DashboardProps):
    def __init__(
        self,
        *,
        dashboard_name: typing.Optional[builtins.str] = None,
        end: typing.Optional[builtins.str] = None,
        period_override: typing.Optional[aws_cdk.aws_cloudwatch.PeriodOverride] = None,
        start: typing.Optional[builtins.str] = None,
        widgets: typing.Optional[typing.Sequence[typing.Sequence[aws_cdk.aws_cloudwatch.IWidget]]] = None,
        auto_scaling: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_autoscaling.AutoScalingGroup, aws_cdk.aws_autoscaling.CfnAutoScalingGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, typing.Sequence[jsii.Number]]]]]] = None,
        elasticache: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_elasticache.CfnReplicationGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]]]] = None,
        load_balancer: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer, aws_cdk.aws_elasticloadbalancingv2.CfnLoadBalancer, typing.Mapping[builtins.str, builtins.str]]]] = None,
        rds: typing.Optional[typing.Sequence[aws_cdk.aws_rds.CfnDBCluster]] = None,
    ) -> None:
        '''
        :param dashboard_name: Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets
        :param auto_scaling: List of AutoScaling. If set, must only contain a list of AutoScaling or Dictionary "{ 'name': string, 'max_capacity': number }" Default: - None
        :param elasticache: List of Elasticache. If set, must only contain a list of Elasticache or Dictionary "{ 'name': string, 'nodes': number }" with nodes being optional Default: - None
        :param load_balancer: List of LoadBalancers. If set, must only contain a list of LoadBalancer or Dictionary "{ 'name': string, 'full_name': string }" Default: - None
        :param rds: List of RDS. If set, must only contain a list of RDS Default: - None
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name
        if end is not None:
            self._values["end"] = end
        if period_override is not None:
            self._values["period_override"] = period_override
        if start is not None:
            self._values["start"] = start
        if widgets is not None:
            self._values["widgets"] = widgets
        if auto_scaling is not None:
            self._values["auto_scaling"] = auto_scaling
        if elasticache is not None:
            self._values["elasticache"] = elasticache
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if rds is not None:
            self._values["rds"] = rds

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''Name of the dashboard.

        If set, must only contain alphanumerics, dash (-) and underscore (_)

        :default: - automatically generated name
        '''
        result = self._values.get("dashboard_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''The end of the time range to use for each widget on the dashboard when the dashboard loads.

        If you specify a value for end, you must also specify a value for start.
        Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        :default: When the dashboard loads, the end date will be the current time.
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period_override(self) -> typing.Optional[aws_cdk.aws_cloudwatch.PeriodOverride]:
        '''Use this field to specify the period for the graphs when the dashboard loads.

        Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard.
        Specifying ``Inherit`` ensures that the period set for each graph is always obeyed.

        :default: Auto
        '''
        result = self._values.get("period_override")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.PeriodOverride], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''The start of the time range to use for each widget on the dashboard.

        You can specify start without specifying end to specify a relative time range that ends with the current time.
        In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for
        minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months.
        You can also use start along with an end field, to specify an absolute time range.
        When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        :default: When the dashboard loads, the start time will be the default time range.
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def widgets(
        self,
    ) -> typing.Optional[typing.List[typing.List[aws_cdk.aws_cloudwatch.IWidget]]]:
        '''Initial set of widgets on the dashboard.

        One array represents a row of widgets.

        :default: - No widgets
        '''
        result = self._values.get("widgets")
        return typing.cast(typing.Optional[typing.List[typing.List[aws_cdk.aws_cloudwatch.IWidget]]], result)

    @builtins.property
    def auto_scaling(
        self,
    ) -> typing.Optional[typing.List[typing.Union[aws_cdk.aws_autoscaling.AutoScalingGroup, aws_cdk.aws_autoscaling.CfnAutoScalingGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, typing.List[jsii.Number]]]]]]:
        '''List of AutoScaling.

        If set, must only contain a list of AutoScaling or Dictionary "{ 'name': string, 'max_capacity': number }"

        :default: - None
        '''
        result = self._values.get("auto_scaling")
        return typing.cast(typing.Optional[typing.List[typing.Union[aws_cdk.aws_autoscaling.AutoScalingGroup, aws_cdk.aws_autoscaling.CfnAutoScalingGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, typing.List[jsii.Number]]]]]], result)

    @builtins.property
    def elasticache(
        self,
    ) -> typing.Optional[typing.List[typing.Union[aws_cdk.aws_elasticache.CfnReplicationGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]]]]:
        '''List of Elasticache.

        If set, must only contain a list of Elasticache or Dictionary "{ 'name': string, 'nodes': number }" with nodes being optional

        :default: - None
        '''
        result = self._values.get("elasticache")
        return typing.cast(typing.Optional[typing.List[typing.Union[aws_cdk.aws_elasticache.CfnReplicationGroup, typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]]]], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[typing.List[typing.Union[aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer, aws_cdk.aws_elasticloadbalancingv2.CfnLoadBalancer, typing.Mapping[builtins.str, builtins.str]]]]:
        '''List of LoadBalancers.

        If set, must only contain a list of LoadBalancer or Dictionary "{ 'name': string, 'full_name': string }"

        :default: - None
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[typing.List[typing.Union[aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer, aws_cdk.aws_elasticloadbalancingv2.CfnLoadBalancer, typing.Mapping[builtins.str, builtins.str]]]], result)

    @builtins.property
    def rds(self) -> typing.Optional[typing.List[aws_cdk.aws_rds.CfnDBCluster]]:
        '''List of RDS.

        If set, must only contain a list of RDS

        :default: - None
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_rds.CfnDBCluster]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HalloumiDashboard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Dashboard",
    "HalloumiDashboard",
]

publication.publish()
