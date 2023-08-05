# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['AccessPolicyArgs', 'AccessPolicy']

@pulumi.input_type
class AccessPolicyArgs:
    def __init__(__self__, *,
                 access_policy_identity: pulumi.Input['AccessPolicyIdentityArgs'],
                 access_policy_permission: pulumi.Input[str],
                 access_policy_resource: pulumi.Input['AccessPolicyResourceArgs']):
        """
        The set of arguments for constructing a AccessPolicy resource.
        :param pulumi.Input['AccessPolicyIdentityArgs'] access_policy_identity: The identity for this access policy. Choose either a user or a group but not both.
        :param pulumi.Input[str] access_policy_permission: The permission level for this access policy. Valid values are ADMINISTRATOR or VIEWER.
        :param pulumi.Input['AccessPolicyResourceArgs'] access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy. Choose either portal or project but not both.
        """
        pulumi.set(__self__, "access_policy_identity", access_policy_identity)
        pulumi.set(__self__, "access_policy_permission", access_policy_permission)
        pulumi.set(__self__, "access_policy_resource", access_policy_resource)

    @property
    @pulumi.getter(name="accessPolicyIdentity")
    def access_policy_identity(self) -> pulumi.Input['AccessPolicyIdentityArgs']:
        """
        The identity for this access policy. Choose either a user or a group but not both.
        """
        return pulumi.get(self, "access_policy_identity")

    @access_policy_identity.setter
    def access_policy_identity(self, value: pulumi.Input['AccessPolicyIdentityArgs']):
        pulumi.set(self, "access_policy_identity", value)

    @property
    @pulumi.getter(name="accessPolicyPermission")
    def access_policy_permission(self) -> pulumi.Input[str]:
        """
        The permission level for this access policy. Valid values are ADMINISTRATOR or VIEWER.
        """
        return pulumi.get(self, "access_policy_permission")

    @access_policy_permission.setter
    def access_policy_permission(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_policy_permission", value)

    @property
    @pulumi.getter(name="accessPolicyResource")
    def access_policy_resource(self) -> pulumi.Input['AccessPolicyResourceArgs']:
        """
        The AWS IoT SiteWise Monitor resource for this access policy. Choose either portal or project but not both.
        """
        return pulumi.get(self, "access_policy_resource")

    @access_policy_resource.setter
    def access_policy_resource(self, value: pulumi.Input['AccessPolicyResourceArgs']):
        pulumi.set(self, "access_policy_resource", value)


class AccessPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy_identity: Optional[pulumi.Input[pulumi.InputType['AccessPolicyIdentityArgs']]] = None,
                 access_policy_permission: Optional[pulumi.Input[str]] = None,
                 access_policy_resource: Optional[pulumi.Input[pulumi.InputType['AccessPolicyResourceArgs']]] = None,
                 __props__=None):
        """
        Resource schema for AWS::IoTSiteWise::AccessPolicy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AccessPolicyIdentityArgs']] access_policy_identity: The identity for this access policy. Choose either a user or a group but not both.
        :param pulumi.Input[str] access_policy_permission: The permission level for this access policy. Valid values are ADMINISTRATOR or VIEWER.
        :param pulumi.Input[pulumi.InputType['AccessPolicyResourceArgs']] access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy. Choose either portal or project but not both.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::IoTSiteWise::AccessPolicy

        :param str resource_name: The name of the resource.
        :param AccessPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy_identity: Optional[pulumi.Input[pulumi.InputType['AccessPolicyIdentityArgs']]] = None,
                 access_policy_permission: Optional[pulumi.Input[str]] = None,
                 access_policy_resource: Optional[pulumi.Input[pulumi.InputType['AccessPolicyResourceArgs']]] = None,
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
            __props__ = AccessPolicyArgs.__new__(AccessPolicyArgs)

            if access_policy_identity is None and not opts.urn:
                raise TypeError("Missing required property 'access_policy_identity'")
            __props__.__dict__["access_policy_identity"] = access_policy_identity
            if access_policy_permission is None and not opts.urn:
                raise TypeError("Missing required property 'access_policy_permission'")
            __props__.__dict__["access_policy_permission"] = access_policy_permission
            if access_policy_resource is None and not opts.urn:
                raise TypeError("Missing required property 'access_policy_resource'")
            __props__.__dict__["access_policy_resource"] = access_policy_resource
            __props__.__dict__["access_policy_arn"] = None
            __props__.__dict__["access_policy_id"] = None
        super(AccessPolicy, __self__).__init__(
            'aws-native:iotsitewise:AccessPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AccessPolicy':
        """
        Get an existing AccessPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AccessPolicyArgs.__new__(AccessPolicyArgs)

        __props__.__dict__["access_policy_arn"] = None
        __props__.__dict__["access_policy_id"] = None
        __props__.__dict__["access_policy_identity"] = None
        __props__.__dict__["access_policy_permission"] = None
        __props__.__dict__["access_policy_resource"] = None
        return AccessPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessPolicyArn")
    def access_policy_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the access policy.
        """
        return pulumi.get(self, "access_policy_arn")

    @property
    @pulumi.getter(name="accessPolicyId")
    def access_policy_id(self) -> pulumi.Output[str]:
        """
        The ID of the access policy.
        """
        return pulumi.get(self, "access_policy_id")

    @property
    @pulumi.getter(name="accessPolicyIdentity")
    def access_policy_identity(self) -> pulumi.Output['outputs.AccessPolicyIdentity']:
        """
        The identity for this access policy. Choose either a user or a group but not both.
        """
        return pulumi.get(self, "access_policy_identity")

    @property
    @pulumi.getter(name="accessPolicyPermission")
    def access_policy_permission(self) -> pulumi.Output[str]:
        """
        The permission level for this access policy. Valid values are ADMINISTRATOR or VIEWER.
        """
        return pulumi.get(self, "access_policy_permission")

    @property
    @pulumi.getter(name="accessPolicyResource")
    def access_policy_resource(self) -> pulumi.Output['outputs.AccessPolicyResource']:
        """
        The AWS IoT SiteWise Monitor resource for this access policy. Choose either portal or project but not both.
        """
        return pulumi.get(self, "access_policy_resource")

