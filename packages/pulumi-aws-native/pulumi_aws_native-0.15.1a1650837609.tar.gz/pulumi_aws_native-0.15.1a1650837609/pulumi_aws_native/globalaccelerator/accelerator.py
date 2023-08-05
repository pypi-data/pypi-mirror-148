# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['AcceleratorArgs', 'Accelerator']

@pulumi.input_type
class AcceleratorArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 ip_address_type: Optional[pulumi.Input['AcceleratorIpAddressType']] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['AcceleratorTagArgs']]]] = None):
        """
        The set of arguments for constructing a Accelerator resource.
        :param pulumi.Input[bool] enabled: Indicates whether an accelerator is enabled. The value is true or false.
        :param pulumi.Input['AcceleratorIpAddressType'] ip_address_type: IP Address type.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: The IP addresses from BYOIP Prefix pool.
        :param pulumi.Input[str] name: Name of accelerator.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if ip_address_type is not None:
            pulumi.set(__self__, "ip_address_type", ip_address_type)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether an accelerator is enabled. The value is true or false.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> Optional[pulumi.Input['AcceleratorIpAddressType']]:
        """
        IP Address type.
        """
        return pulumi.get(self, "ip_address_type")

    @ip_address_type.setter
    def ip_address_type(self, value: Optional[pulumi.Input['AcceleratorIpAddressType']]):
        pulumi.set(self, "ip_address_type", value)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IP addresses from BYOIP Prefix pool.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of accelerator.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AcceleratorTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AcceleratorTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Accelerator(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 ip_address_type: Optional[pulumi.Input['AcceleratorIpAddressType']] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AcceleratorTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::GlobalAccelerator::Accelerator

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Indicates whether an accelerator is enabled. The value is true or false.
        :param pulumi.Input['AcceleratorIpAddressType'] ip_address_type: IP Address type.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: The IP addresses from BYOIP Prefix pool.
        :param pulumi.Input[str] name: Name of accelerator.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AcceleratorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::GlobalAccelerator::Accelerator

        :param str resource_name: The name of the resource.
        :param AcceleratorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AcceleratorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 ip_address_type: Optional[pulumi.Input['AcceleratorIpAddressType']] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AcceleratorTagArgs']]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AcceleratorArgs.__new__(AcceleratorArgs)

            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["ip_address_type"] = ip_address_type
            __props__.__dict__["ip_addresses"] = ip_addresses
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["accelerator_arn"] = None
            __props__.__dict__["dns_name"] = None
        super(Accelerator, __self__).__init__(
            'aws-native:globalaccelerator:Accelerator',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Accelerator':
        """
        Get an existing Accelerator resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AcceleratorArgs.__new__(AcceleratorArgs)

        __props__.__dict__["accelerator_arn"] = None
        __props__.__dict__["dns_name"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["ip_address_type"] = None
        __props__.__dict__["ip_addresses"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        return Accelerator(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorArn")
    def accelerator_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the accelerator.
        """
        return pulumi.get(self, "accelerator_arn")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> pulumi.Output[str]:
        """
        The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether an accelerator is enabled. The value is true or false.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> pulumi.Output[Optional['AcceleratorIpAddressType']]:
        """
        IP Address type.
        """
        return pulumi.get(self, "ip_address_type")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The IP addresses from BYOIP Prefix pool.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of accelerator.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.AcceleratorTag']]]:
        return pulumi.get(self, "tags")

