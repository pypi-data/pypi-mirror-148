# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'LoadBalancerAccessLoggingPolicyArgs',
    'LoadBalancerAppCookieStickinessPolicyArgs',
    'LoadBalancerConnectionDrainingPolicyArgs',
    'LoadBalancerConnectionSettingsArgs',
    'LoadBalancerHealthCheckArgs',
    'LoadBalancerLBCookieStickinessPolicyArgs',
    'LoadBalancerListenersArgs',
    'LoadBalancerPoliciesArgs',
    'LoadBalancerTagArgs',
]

@pulumi.input_type
class LoadBalancerAccessLoggingPolicyArgs:
    def __init__(__self__, *,
                 enabled: pulumi.Input[bool],
                 s3_bucket_name: pulumi.Input[str],
                 emit_interval: Optional[pulumi.Input[int]] = None,
                 s3_bucket_prefix: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "s3_bucket_name", s3_bucket_name)
        if emit_interval is not None:
            pulumi.set(__self__, "emit_interval", emit_interval)
        if s3_bucket_prefix is not None:
            pulumi.set(__self__, "s3_bucket_prefix", s3_bucket_prefix)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "s3_bucket_name")

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket_name", value)

    @property
    @pulumi.getter(name="emitInterval")
    def emit_interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "emit_interval")

    @emit_interval.setter
    def emit_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "emit_interval", value)

    @property
    @pulumi.getter(name="s3BucketPrefix")
    def s3_bucket_prefix(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "s3_bucket_prefix")

    @s3_bucket_prefix.setter
    def s3_bucket_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_bucket_prefix", value)


@pulumi.input_type
class LoadBalancerAppCookieStickinessPolicyArgs:
    def __init__(__self__, *,
                 cookie_name: pulumi.Input[str],
                 policy_name: pulumi.Input[str]):
        pulumi.set(__self__, "cookie_name", cookie_name)
        pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="cookieName")
    def cookie_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "cookie_name")

    @cookie_name.setter
    def cookie_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cookie_name", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)


@pulumi.input_type
class LoadBalancerConnectionDrainingPolicyArgs:
    def __init__(__self__, *,
                 enabled: pulumi.Input[bool],
                 timeout: Optional[pulumi.Input[int]] = None):
        pulumi.set(__self__, "enabled", enabled)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)


@pulumi.input_type
class LoadBalancerConnectionSettingsArgs:
    def __init__(__self__, *,
                 idle_timeout: pulumi.Input[int]):
        pulumi.set(__self__, "idle_timeout", idle_timeout)

    @property
    @pulumi.getter(name="idleTimeout")
    def idle_timeout(self) -> pulumi.Input[int]:
        return pulumi.get(self, "idle_timeout")

    @idle_timeout.setter
    def idle_timeout(self, value: pulumi.Input[int]):
        pulumi.set(self, "idle_timeout", value)


@pulumi.input_type
class LoadBalancerHealthCheckArgs:
    def __init__(__self__, *,
                 healthy_threshold: pulumi.Input[str],
                 interval: pulumi.Input[str],
                 target: pulumi.Input[str],
                 timeout: pulumi.Input[str],
                 unhealthy_threshold: pulumi.Input[str]):
        pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        pulumi.set(__self__, "interval", interval)
        pulumi.set(__self__, "target", target)
        pulumi.set(__self__, "timeout", timeout)
        pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> pulumi.Input[str]:
        return pulumi.get(self, "healthy_threshold")

    @healthy_threshold.setter
    def healthy_threshold(self, value: pulumi.Input[str]):
        pulumi.set(self, "healthy_threshold", value)

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Input[str]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: pulumi.Input[str]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter
    def timeout(self) -> pulumi.Input[str]:
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: pulumi.Input[str]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> pulumi.Input[str]:
        return pulumi.get(self, "unhealthy_threshold")

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: pulumi.Input[str]):
        pulumi.set(self, "unhealthy_threshold", value)


@pulumi.input_type
class LoadBalancerLBCookieStickinessPolicyArgs:
    def __init__(__self__, *,
                 cookie_expiration_period: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None):
        if cookie_expiration_period is not None:
            pulumi.set(__self__, "cookie_expiration_period", cookie_expiration_period)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="cookieExpirationPeriod")
    def cookie_expiration_period(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cookie_expiration_period")

    @cookie_expiration_period.setter
    def cookie_expiration_period(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cookie_expiration_period", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)


@pulumi.input_type
class LoadBalancerListenersArgs:
    def __init__(__self__, *,
                 instance_port: pulumi.Input[str],
                 load_balancer_port: pulumi.Input[str],
                 protocol: pulumi.Input[str],
                 instance_protocol: Optional[pulumi.Input[str]] = None,
                 policy_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 s_sl_certificate_id: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "instance_port", instance_port)
        pulumi.set(__self__, "load_balancer_port", load_balancer_port)
        pulumi.set(__self__, "protocol", protocol)
        if instance_protocol is not None:
            pulumi.set(__self__, "instance_protocol", instance_protocol)
        if policy_names is not None:
            pulumi.set(__self__, "policy_names", policy_names)
        if s_sl_certificate_id is not None:
            pulumi.set(__self__, "s_sl_certificate_id", s_sl_certificate_id)

    @property
    @pulumi.getter(name="instancePort")
    def instance_port(self) -> pulumi.Input[str]:
        return pulumi.get(self, "instance_port")

    @instance_port.setter
    def instance_port(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_port", value)

    @property
    @pulumi.getter(name="loadBalancerPort")
    def load_balancer_port(self) -> pulumi.Input[str]:
        return pulumi.get(self, "load_balancer_port")

    @load_balancer_port.setter
    def load_balancer_port(self, value: pulumi.Input[str]):
        pulumi.set(self, "load_balancer_port", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[str]:
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="instanceProtocol")
    def instance_protocol(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "instance_protocol")

    @instance_protocol.setter
    def instance_protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_protocol", value)

    @property
    @pulumi.getter(name="policyNames")
    def policy_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "policy_names")

    @policy_names.setter
    def policy_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "policy_names", value)

    @property
    @pulumi.getter(name="sSLCertificateId")
    def s_sl_certificate_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "s_sl_certificate_id")

    @s_sl_certificate_id.setter
    def s_sl_certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s_sl_certificate_id", value)


@pulumi.input_type
class LoadBalancerPoliciesArgs:
    def __init__(__self__, *,
                 attributes: pulumi.Input[Sequence[Any]],
                 policy_name: pulumi.Input[str],
                 policy_type: pulumi.Input[str],
                 instance_ports: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 load_balancer_ports: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        pulumi.set(__self__, "attributes", attributes)
        pulumi.set(__self__, "policy_name", policy_name)
        pulumi.set(__self__, "policy_type", policy_type)
        if instance_ports is not None:
            pulumi.set(__self__, "instance_ports", instance_ports)
        if load_balancer_ports is not None:
            pulumi.set(__self__, "load_balancer_ports", load_balancer_ports)

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Input[Sequence[Any]]:
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: pulumi.Input[Sequence[Any]]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "policy_type")

    @policy_type.setter
    def policy_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_type", value)

    @property
    @pulumi.getter(name="instancePorts")
    def instance_ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "instance_ports")

    @instance_ports.setter
    def instance_ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "instance_ports", value)

    @property
    @pulumi.getter(name="loadBalancerPorts")
    def load_balancer_ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "load_balancer_ports")

    @load_balancer_ports.setter
    def load_balancer_ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "load_balancer_ports", value)


@pulumi.input_type
class LoadBalancerTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


