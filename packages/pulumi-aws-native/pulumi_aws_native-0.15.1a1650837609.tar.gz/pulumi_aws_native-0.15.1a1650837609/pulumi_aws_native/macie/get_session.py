# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'GetSessionResult',
    'AwaitableGetSessionResult',
    'get_session',
    'get_session_output',
]

@pulumi.output_type
class GetSessionResult:
    def __init__(__self__, aws_account_id=None, finding_publishing_frequency=None, service_role=None, status=None):
        if aws_account_id and not isinstance(aws_account_id, str):
            raise TypeError("Expected argument 'aws_account_id' to be a str")
        pulumi.set(__self__, "aws_account_id", aws_account_id)
        if finding_publishing_frequency and not isinstance(finding_publishing_frequency, str):
            raise TypeError("Expected argument 'finding_publishing_frequency' to be a str")
        pulumi.set(__self__, "finding_publishing_frequency", finding_publishing_frequency)
        if service_role and not isinstance(service_role, str):
            raise TypeError("Expected argument 'service_role' to be a str")
        pulumi.set(__self__, "service_role", service_role)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[str]:
        """
        AWS account ID of customer
        """
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter(name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> Optional['SessionFindingPublishingFrequency']:
        """
        A enumeration value that specifies how frequently finding updates are published.
        """
        return pulumi.get(self, "finding_publishing_frequency")

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> Optional[str]:
        """
        Service role used by Macie
        """
        return pulumi.get(self, "service_role")

    @property
    @pulumi.getter
    def status(self) -> Optional['SessionStatus']:
        """
        A enumeration value that specifies the status of the Macie Session.
        """
        return pulumi.get(self, "status")


class AwaitableGetSessionResult(GetSessionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSessionResult(
            aws_account_id=self.aws_account_id,
            finding_publishing_frequency=self.finding_publishing_frequency,
            service_role=self.service_role,
            status=self.status)


def get_session(aws_account_id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSessionResult:
    """
    The AWS::Macie::Session resource specifies a new Amazon Macie session. A session is an object that represents the Amazon Macie service. A session is required for Amazon Macie to become operational.


    :param str aws_account_id: AWS account ID of customer
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:macie:getSession', __args__, opts=opts, typ=GetSessionResult).value

    return AwaitableGetSessionResult(
        aws_account_id=__ret__.aws_account_id,
        finding_publishing_frequency=__ret__.finding_publishing_frequency,
        service_role=__ret__.service_role,
        status=__ret__.status)


@_utilities.lift_output_func(get_session)
def get_session_output(aws_account_id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSessionResult]:
    """
    The AWS::Macie::Session resource specifies a new Amazon Macie session. A session is an object that represents the Amazon Macie service. A session is required for Amazon Macie to become operational.


    :param str aws_account_id: AWS account ID of customer
    """
    ...
