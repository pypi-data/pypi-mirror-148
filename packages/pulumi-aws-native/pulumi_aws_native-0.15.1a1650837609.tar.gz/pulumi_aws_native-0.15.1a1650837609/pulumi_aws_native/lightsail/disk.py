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

__all__ = ['DiskArgs', 'Disk']

@pulumi.input_type
class DiskArgs:
    def __init__(__self__, *,
                 size_in_gb: pulumi.Input[int],
                 add_ons: Optional[pulumi.Input[Sequence[pulumi.Input['DiskAddOnArgs']]]] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 disk_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['DiskTagArgs']]]] = None):
        """
        The set of arguments for constructing a Disk resource.
        :param pulumi.Input[int] size_in_gb: Size of the Lightsail disk
        :param pulumi.Input[Sequence[pulumi.Input['DiskAddOnArgs']]] add_ons: An array of objects representing the add-ons to enable for the new instance.
        :param pulumi.Input[str] availability_zone: The Availability Zone in which to create your instance. Use the following format: us-east-2a (case sensitive). Be sure to add the include Availability Zones parameter to your request.
        :param pulumi.Input[str] disk_name: The names to use for your new Lightsail disk.
        :param pulumi.Input[Sequence[pulumi.Input['DiskTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "size_in_gb", size_in_gb)
        if add_ons is not None:
            pulumi.set(__self__, "add_ons", add_ons)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if disk_name is not None:
            pulumi.set(__self__, "disk_name", disk_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="sizeInGb")
    def size_in_gb(self) -> pulumi.Input[int]:
        """
        Size of the Lightsail disk
        """
        return pulumi.get(self, "size_in_gb")

    @size_in_gb.setter
    def size_in_gb(self, value: pulumi.Input[int]):
        pulumi.set(self, "size_in_gb", value)

    @property
    @pulumi.getter(name="addOns")
    def add_ons(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DiskAddOnArgs']]]]:
        """
        An array of objects representing the add-ons to enable for the new instance.
        """
        return pulumi.get(self, "add_ons")

    @add_ons.setter
    def add_ons(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DiskAddOnArgs']]]]):
        pulumi.set(self, "add_ons", value)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        The Availability Zone in which to create your instance. Use the following format: us-east-2a (case sensitive). Be sure to add the include Availability Zones parameter to your request.
        """
        return pulumi.get(self, "availability_zone")

    @availability_zone.setter
    def availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_zone", value)

    @property
    @pulumi.getter(name="diskName")
    def disk_name(self) -> Optional[pulumi.Input[str]]:
        """
        The names to use for your new Lightsail disk.
        """
        return pulumi.get(self, "disk_name")

    @disk_name.setter
    def disk_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DiskTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DiskTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Disk(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 add_ons: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DiskAddOnArgs']]]]] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 disk_name: Optional[pulumi.Input[str]] = None,
                 size_in_gb: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DiskTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Lightsail::Disk

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DiskAddOnArgs']]]] add_ons: An array of objects representing the add-ons to enable for the new instance.
        :param pulumi.Input[str] availability_zone: The Availability Zone in which to create your instance. Use the following format: us-east-2a (case sensitive). Be sure to add the include Availability Zones parameter to your request.
        :param pulumi.Input[str] disk_name: The names to use for your new Lightsail disk.
        :param pulumi.Input[int] size_in_gb: Size of the Lightsail disk
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DiskTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DiskArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Lightsail::Disk

        :param str resource_name: The name of the resource.
        :param DiskArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DiskArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 add_ons: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DiskAddOnArgs']]]]] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 disk_name: Optional[pulumi.Input[str]] = None,
                 size_in_gb: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DiskTagArgs']]]]] = None,
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
            __props__ = DiskArgs.__new__(DiskArgs)

            __props__.__dict__["add_ons"] = add_ons
            __props__.__dict__["availability_zone"] = availability_zone
            __props__.__dict__["disk_name"] = disk_name
            if size_in_gb is None and not opts.urn:
                raise TypeError("Missing required property 'size_in_gb'")
            __props__.__dict__["size_in_gb"] = size_in_gb
            __props__.__dict__["tags"] = tags
            __props__.__dict__["attached_to"] = None
            __props__.__dict__["attachment_state"] = None
            __props__.__dict__["disk_arn"] = None
            __props__.__dict__["iops"] = None
            __props__.__dict__["is_attached"] = None
            __props__.__dict__["location"] = None
            __props__.__dict__["path"] = None
            __props__.__dict__["resource_type"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["support_code"] = None
        super(Disk, __self__).__init__(
            'aws-native:lightsail:Disk',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Disk':
        """
        Get an existing Disk resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DiskArgs.__new__(DiskArgs)

        __props__.__dict__["add_ons"] = None
        __props__.__dict__["attached_to"] = None
        __props__.__dict__["attachment_state"] = None
        __props__.__dict__["availability_zone"] = None
        __props__.__dict__["disk_arn"] = None
        __props__.__dict__["disk_name"] = None
        __props__.__dict__["iops"] = None
        __props__.__dict__["is_attached"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["path"] = None
        __props__.__dict__["resource_type"] = None
        __props__.__dict__["size_in_gb"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["support_code"] = None
        __props__.__dict__["tags"] = None
        return Disk(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addOns")
    def add_ons(self) -> pulumi.Output[Optional[Sequence['outputs.DiskAddOn']]]:
        """
        An array of objects representing the add-ons to enable for the new instance.
        """
        return pulumi.get(self, "add_ons")

    @property
    @pulumi.getter(name="attachedTo")
    def attached_to(self) -> pulumi.Output[str]:
        """
        Name of the attached Lightsail Instance
        """
        return pulumi.get(self, "attached_to")

    @property
    @pulumi.getter(name="attachmentState")
    def attachment_state(self) -> pulumi.Output[str]:
        """
        Attachment State of the Lightsail disk
        """
        return pulumi.get(self, "attachment_state")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> pulumi.Output[Optional[str]]:
        """
        The Availability Zone in which to create your instance. Use the following format: us-east-2a (case sensitive). Be sure to add the include Availability Zones parameter to your request.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="diskArn")
    def disk_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "disk_arn")

    @property
    @pulumi.getter(name="diskName")
    def disk_name(self) -> pulumi.Output[str]:
        """
        The names to use for your new Lightsail disk.
        """
        return pulumi.get(self, "disk_name")

    @property
    @pulumi.getter
    def iops(self) -> pulumi.Output[int]:
        """
        Iops of the Lightsail disk
        """
        return pulumi.get(self, "iops")

    @property
    @pulumi.getter(name="isAttached")
    def is_attached(self) -> pulumi.Output[bool]:
        """
        Check is Disk is attached state
        """
        return pulumi.get(self, "is_attached")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output['outputs.DiskLocation']:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[str]:
        """
        Path of the  attached Disk
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[str]:
        """
        Resource type of Lightsail instance.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="sizeInGb")
    def size_in_gb(self) -> pulumi.Output[int]:
        """
        Size of the Lightsail disk
        """
        return pulumi.get(self, "size_in_gb")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the Lightsail disk
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="supportCode")
    def support_code(self) -> pulumi.Output[str]:
        """
        Support code to help identify any issues
        """
        return pulumi.get(self, "support_code")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.DiskTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

