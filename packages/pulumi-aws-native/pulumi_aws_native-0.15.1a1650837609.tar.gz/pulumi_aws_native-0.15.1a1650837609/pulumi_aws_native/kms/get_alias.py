# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetAliasResult',
    'AwaitableGetAliasResult',
    'get_alias',
    'get_alias_output',
]

@pulumi.output_type
class GetAliasResult:
    def __init__(__self__, target_key_id=None):
        if target_key_id and not isinstance(target_key_id, str):
            raise TypeError("Expected argument 'target_key_id' to be a str")
        pulumi.set(__self__, "target_key_id", target_key_id)

    @property
    @pulumi.getter(name="targetKeyId")
    def target_key_id(self) -> Optional[str]:
        """
        Identifies the CMK to which the alias refers. Specify the key ID or the Amazon Resource Name (ARN) of the CMK. You cannot specify another alias. For help finding the key ID and ARN, see Finding the Key ID and ARN in the AWS Key Management Service Developer Guide.
        """
        return pulumi.get(self, "target_key_id")


class AwaitableGetAliasResult(GetAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAliasResult(
            target_key_id=self.target_key_id)


def get_alias(alias_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAliasResult:
    """
    The AWS::KMS::Alias resource specifies a display name for a customer master key (CMK) in AWS Key Management Service (AWS KMS). You can use an alias to identify a CMK in cryptographic operations.


    :param str alias_name: Specifies the alias name. This value must begin with alias/ followed by a name, such as alias/ExampleAlias. The alias name cannot begin with alias/aws/. The alias/aws/ prefix is reserved for AWS managed CMKs.
    """
    __args__ = dict()
    __args__['aliasName'] = alias_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:kms:getAlias', __args__, opts=opts, typ=GetAliasResult).value

    return AwaitableGetAliasResult(
        target_key_id=__ret__.target_key_id)


@_utilities.lift_output_func(get_alias)
def get_alias_output(alias_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAliasResult]:
    """
    The AWS::KMS::Alias resource specifies a display name for a customer master key (CMK) in AWS Key Management Service (AWS KMS). You can use an alias to identify a CMK in cryptographic operations.


    :param str alias_name: Specifies the alias name. This value must begin with alias/ followed by a name, such as alias/ExampleAlias. The alias name cannot begin with alias/aws/. The alias/aws/ prefix is reserved for AWS managed CMKs.
    """
    ...
