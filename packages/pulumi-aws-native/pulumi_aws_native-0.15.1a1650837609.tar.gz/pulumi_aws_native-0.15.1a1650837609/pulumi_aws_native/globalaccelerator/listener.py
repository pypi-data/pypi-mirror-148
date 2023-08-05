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

__all__ = ['ListenerArgs', 'Listener']

@pulumi.input_type
class ListenerArgs:
    def __init__(__self__, *,
                 accelerator_arn: pulumi.Input[str],
                 port_ranges: pulumi.Input[Sequence[pulumi.Input['ListenerPortRangeArgs']]],
                 protocol: pulumi.Input['ListenerProtocol'],
                 client_affinity: Optional[pulumi.Input['ListenerClientAffinity']] = None):
        """
        The set of arguments for constructing a Listener resource.
        :param pulumi.Input[str] accelerator_arn: The Amazon Resource Name (ARN) of the accelerator.
        :param pulumi.Input['ListenerProtocol'] protocol: The protocol for the listener.
        :param pulumi.Input['ListenerClientAffinity'] client_affinity: Client affinity lets you direct all requests from a user to the same endpoint.
        """
        pulumi.set(__self__, "accelerator_arn", accelerator_arn)
        pulumi.set(__self__, "port_ranges", port_ranges)
        pulumi.set(__self__, "protocol", protocol)
        if client_affinity is not None:
            pulumi.set(__self__, "client_affinity", client_affinity)

    @property
    @pulumi.getter(name="acceleratorArn")
    def accelerator_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the accelerator.
        """
        return pulumi.get(self, "accelerator_arn")

    @accelerator_arn.setter
    def accelerator_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "accelerator_arn", value)

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> pulumi.Input[Sequence[pulumi.Input['ListenerPortRangeArgs']]]:
        return pulumi.get(self, "port_ranges")

    @port_ranges.setter
    def port_ranges(self, value: pulumi.Input[Sequence[pulumi.Input['ListenerPortRangeArgs']]]):
        pulumi.set(self, "port_ranges", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input['ListenerProtocol']:
        """
        The protocol for the listener.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input['ListenerProtocol']):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="clientAffinity")
    def client_affinity(self) -> Optional[pulumi.Input['ListenerClientAffinity']]:
        """
        Client affinity lets you direct all requests from a user to the same endpoint.
        """
        return pulumi.get(self, "client_affinity")

    @client_affinity.setter
    def client_affinity(self, value: Optional[pulumi.Input['ListenerClientAffinity']]):
        pulumi.set(self, "client_affinity", value)


class Listener(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_arn: Optional[pulumi.Input[str]] = None,
                 client_affinity: Optional[pulumi.Input['ListenerClientAffinity']] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ListenerPortRangeArgs']]]]] = None,
                 protocol: Optional[pulumi.Input['ListenerProtocol']] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::GlobalAccelerator::Listener

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_arn: The Amazon Resource Name (ARN) of the accelerator.
        :param pulumi.Input['ListenerClientAffinity'] client_affinity: Client affinity lets you direct all requests from a user to the same endpoint.
        :param pulumi.Input['ListenerProtocol'] protocol: The protocol for the listener.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ListenerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::GlobalAccelerator::Listener

        :param str resource_name: The name of the resource.
        :param ListenerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ListenerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_arn: Optional[pulumi.Input[str]] = None,
                 client_affinity: Optional[pulumi.Input['ListenerClientAffinity']] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ListenerPortRangeArgs']]]]] = None,
                 protocol: Optional[pulumi.Input['ListenerProtocol']] = None,
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
            __props__ = ListenerArgs.__new__(ListenerArgs)

            if accelerator_arn is None and not opts.urn:
                raise TypeError("Missing required property 'accelerator_arn'")
            __props__.__dict__["accelerator_arn"] = accelerator_arn
            __props__.__dict__["client_affinity"] = client_affinity
            if port_ranges is None and not opts.urn:
                raise TypeError("Missing required property 'port_ranges'")
            __props__.__dict__["port_ranges"] = port_ranges
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["listener_arn"] = None
        super(Listener, __self__).__init__(
            'aws-native:globalaccelerator:Listener',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Listener':
        """
        Get an existing Listener resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ListenerArgs.__new__(ListenerArgs)

        __props__.__dict__["accelerator_arn"] = None
        __props__.__dict__["client_affinity"] = None
        __props__.__dict__["listener_arn"] = None
        __props__.__dict__["port_ranges"] = None
        __props__.__dict__["protocol"] = None
        return Listener(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorArn")
    def accelerator_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the accelerator.
        """
        return pulumi.get(self, "accelerator_arn")

    @property
    @pulumi.getter(name="clientAffinity")
    def client_affinity(self) -> pulumi.Output[Optional['ListenerClientAffinity']]:
        """
        Client affinity lets you direct all requests from a user to the same endpoint.
        """
        return pulumi.get(self, "client_affinity")

    @property
    @pulumi.getter(name="listenerArn")
    def listener_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the listener.
        """
        return pulumi.get(self, "listener_arn")

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> pulumi.Output[Sequence['outputs.ListenerPortRange']]:
        return pulumi.get(self, "port_ranges")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output['ListenerProtocol']:
        """
        The protocol for the listener.
        """
        return pulumi.get(self, "protocol")

