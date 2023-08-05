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

__all__ = [
    'GetAssessmentResult',
    'AwaitableGetAssessmentResult',
    'get_assessment',
    'get_assessment_output',
]

@pulumi.output_type
class GetAssessmentResult:
    def __init__(__self__, arn=None, assessment_id=None, assessment_reports_destination=None, creation_time=None, delegations=None, roles=None, scope=None, status=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if assessment_id and not isinstance(assessment_id, str):
            raise TypeError("Expected argument 'assessment_id' to be a str")
        pulumi.set(__self__, "assessment_id", assessment_id)
        if assessment_reports_destination and not isinstance(assessment_reports_destination, dict):
            raise TypeError("Expected argument 'assessment_reports_destination' to be a dict")
        pulumi.set(__self__, "assessment_reports_destination", assessment_reports_destination)
        if creation_time and not isinstance(creation_time, float):
            raise TypeError("Expected argument 'creation_time' to be a float")
        pulumi.set(__self__, "creation_time", creation_time)
        if delegations and not isinstance(delegations, list):
            raise TypeError("Expected argument 'delegations' to be a list")
        pulumi.set(__self__, "delegations", delegations)
        if roles and not isinstance(roles, list):
            raise TypeError("Expected argument 'roles' to be a list")
        pulumi.set(__self__, "roles", roles)
        if scope and not isinstance(scope, dict):
            raise TypeError("Expected argument 'scope' to be a dict")
        pulumi.set(__self__, "scope", scope)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="assessmentId")
    def assessment_id(self) -> Optional[str]:
        return pulumi.get(self, "assessment_id")

    @property
    @pulumi.getter(name="assessmentReportsDestination")
    def assessment_reports_destination(self) -> Optional['outputs.AssessmentReportsDestination']:
        return pulumi.get(self, "assessment_reports_destination")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[float]:
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def delegations(self) -> Optional[Sequence['outputs.AssessmentDelegation']]:
        """
        The list of delegations.
        """
        return pulumi.get(self, "delegations")

    @property
    @pulumi.getter
    def roles(self) -> Optional[Sequence['outputs.AssessmentRole']]:
        """
        The list of roles for the specified assessment.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter
    def scope(self) -> Optional['outputs.AssessmentScope']:
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def status(self) -> Optional['AssessmentStatus']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.AssessmentTag']]:
        """
        The tags associated with the assessment.
        """
        return pulumi.get(self, "tags")


class AwaitableGetAssessmentResult(GetAssessmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAssessmentResult(
            arn=self.arn,
            assessment_id=self.assessment_id,
            assessment_reports_destination=self.assessment_reports_destination,
            creation_time=self.creation_time,
            delegations=self.delegations,
            roles=self.roles,
            scope=self.scope,
            status=self.status,
            tags=self.tags)


def get_assessment(assessment_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAssessmentResult:
    """
    An entity that defines the scope of audit evidence collected by AWS Audit Manager.
    """
    __args__ = dict()
    __args__['assessmentId'] = assessment_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:auditmanager:getAssessment', __args__, opts=opts, typ=GetAssessmentResult).value

    return AwaitableGetAssessmentResult(
        arn=__ret__.arn,
        assessment_id=__ret__.assessment_id,
        assessment_reports_destination=__ret__.assessment_reports_destination,
        creation_time=__ret__.creation_time,
        delegations=__ret__.delegations,
        roles=__ret__.roles,
        scope=__ret__.scope,
        status=__ret__.status,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_assessment)
def get_assessment_output(assessment_id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAssessmentResult]:
    """
    An entity that defines the scope of audit evidence collected by AWS Audit Manager.
    """
    ...
