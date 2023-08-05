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
    'ServerEndpointDetails',
    'ServerIdentityProviderDetails',
    'ServerProtocol',
    'ServerProtocolDetails',
    'ServerTag',
    'ServerWorkflowDetail',
    'ServerWorkflowDetails',
    'UserHomeDirectoryMapEntry',
    'UserPosixProfile',
    'UserSshPublicKey',
    'UserTag',
    'WorkflowInputFileLocation',
    'WorkflowS3InputFileLocation',
    'WorkflowS3Tag',
    'WorkflowStep',
    'WorkflowStepCopyStepDetailsProperties',
    'WorkflowStepCustomStepDetailsProperties',
    'WorkflowStepDeleteStepDetailsProperties',
    'WorkflowStepTagStepDetailsProperties',
    'WorkflowTag',
]

@pulumi.output_type
class ServerEndpointDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "addressAllocationIds":
            suggest = "address_allocation_ids"
        elif key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "vpcEndpointId":
            suggest = "vpc_endpoint_id"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerEndpointDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerEndpointDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerEndpointDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 address_allocation_ids: Optional[Sequence[str]] = None,
                 security_group_ids: Optional[Sequence[str]] = None,
                 subnet_ids: Optional[Sequence[str]] = None,
                 vpc_endpoint_id: Optional[str] = None,
                 vpc_id: Optional[str] = None):
        if address_allocation_ids is not None:
            pulumi.set(__self__, "address_allocation_ids", address_allocation_ids)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="addressAllocationIds")
    def address_allocation_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "address_allocation_ids")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[str]:
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class ServerIdentityProviderDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "directoryId":
            suggest = "directory_id"
        elif key == "invocationRole":
            suggest = "invocation_role"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerIdentityProviderDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerIdentityProviderDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerIdentityProviderDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 directory_id: Optional[str] = None,
                 function: Optional[str] = None,
                 invocation_role: Optional[str] = None,
                 url: Optional[str] = None):
        if directory_id is not None:
            pulumi.set(__self__, "directory_id", directory_id)
        if function is not None:
            pulumi.set(__self__, "function", function)
        if invocation_role is not None:
            pulumi.set(__self__, "invocation_role", invocation_role)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> Optional[str]:
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter
    def function(self) -> Optional[str]:
        return pulumi.get(self, "function")

    @property
    @pulumi.getter(name="invocationRole")
    def invocation_role(self) -> Optional[str]:
        return pulumi.get(self, "invocation_role")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        return pulumi.get(self, "url")


@pulumi.output_type
class ServerProtocol(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ServerProtocolDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "passiveIp":
            suggest = "passive_ip"
        elif key == "tlsSessionResumptionMode":
            suggest = "tls_session_resumption_mode"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerProtocolDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerProtocolDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerProtocolDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 passive_ip: Optional[str] = None,
                 tls_session_resumption_mode: Optional[str] = None):
        if passive_ip is not None:
            pulumi.set(__self__, "passive_ip", passive_ip)
        if tls_session_resumption_mode is not None:
            pulumi.set(__self__, "tls_session_resumption_mode", tls_session_resumption_mode)

    @property
    @pulumi.getter(name="passiveIp")
    def passive_ip(self) -> Optional[str]:
        return pulumi.get(self, "passive_ip")

    @property
    @pulumi.getter(name="tlsSessionResumptionMode")
    def tls_session_resumption_mode(self) -> Optional[str]:
        return pulumi.get(self, "tls_session_resumption_mode")


@pulumi.output_type
class ServerTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ServerWorkflowDetail(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "executionRole":
            suggest = "execution_role"
        elif key == "workflowId":
            suggest = "workflow_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerWorkflowDetail. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerWorkflowDetail.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerWorkflowDetail.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 execution_role: str,
                 workflow_id: str):
        pulumi.set(__self__, "execution_role", execution_role)
        pulumi.set(__self__, "workflow_id", workflow_id)

    @property
    @pulumi.getter(name="executionRole")
    def execution_role(self) -> str:
        return pulumi.get(self, "execution_role")

    @property
    @pulumi.getter(name="workflowId")
    def workflow_id(self) -> str:
        return pulumi.get(self, "workflow_id")


@pulumi.output_type
class ServerWorkflowDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "onUpload":
            suggest = "on_upload"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerWorkflowDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerWorkflowDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerWorkflowDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 on_upload: Sequence['outputs.ServerWorkflowDetail']):
        pulumi.set(__self__, "on_upload", on_upload)

    @property
    @pulumi.getter(name="onUpload")
    def on_upload(self) -> Sequence['outputs.ServerWorkflowDetail']:
        return pulumi.get(self, "on_upload")


@pulumi.output_type
class UserHomeDirectoryMapEntry(dict):
    def __init__(__self__, *,
                 entry: str,
                 target: str):
        pulumi.set(__self__, "entry", entry)
        pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter
    def entry(self) -> str:
        return pulumi.get(self, "entry")

    @property
    @pulumi.getter
    def target(self) -> str:
        return pulumi.get(self, "target")


@pulumi.output_type
class UserPosixProfile(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "secondaryGids":
            suggest = "secondary_gids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserPosixProfile. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserPosixProfile.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserPosixProfile.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 gid: float,
                 uid: float,
                 secondary_gids: Optional[Sequence[float]] = None):
        pulumi.set(__self__, "gid", gid)
        pulumi.set(__self__, "uid", uid)
        if secondary_gids is not None:
            pulumi.set(__self__, "secondary_gids", secondary_gids)

    @property
    @pulumi.getter
    def gid(self) -> float:
        return pulumi.get(self, "gid")

    @property
    @pulumi.getter
    def uid(self) -> float:
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="secondaryGids")
    def secondary_gids(self) -> Optional[Sequence[float]]:
        return pulumi.get(self, "secondary_gids")


@pulumi.output_type
class UserSshPublicKey(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class UserTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class WorkflowInputFileLocation(dict):
    """
    Specifies the location for the file being copied. Only applicable for the Copy type of workflow steps.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "s3FileLocation":
            suggest = "s3_file_location"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkflowInputFileLocation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkflowInputFileLocation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkflowInputFileLocation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s3_file_location: Optional['outputs.WorkflowS3InputFileLocation'] = None):
        """
        Specifies the location for the file being copied. Only applicable for the Copy type of workflow steps.
        """
        if s3_file_location is not None:
            pulumi.set(__self__, "s3_file_location", s3_file_location)

    @property
    @pulumi.getter(name="s3FileLocation")
    def s3_file_location(self) -> Optional['outputs.WorkflowS3InputFileLocation']:
        return pulumi.get(self, "s3_file_location")


@pulumi.output_type
class WorkflowS3InputFileLocation(dict):
    """
    Specifies the details for the S3 file being copied.
    """
    def __init__(__self__, *,
                 bucket: Optional[str] = None,
                 key: Optional[str] = None):
        """
        Specifies the details for the S3 file being copied.
        :param str bucket: Specifies the S3 bucket that contains the file being copied.
        :param str key: The name assigned to the file when it was created in S3. You use the object key to retrieve the object.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if key is not None:
            pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[str]:
        """
        Specifies the S3 bucket that contains the file being copied.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The name assigned to the file when it was created in S3. You use the object key to retrieve the object.
        """
        return pulumi.get(self, "key")


@pulumi.output_type
class WorkflowS3Tag(dict):
    """
    Specifies the key-value pair that are assigned to a file during the execution of a Tagging step.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        Specifies the key-value pair that are assigned to a file during the execution of a Tagging step.
        :param str key: The name assigned to the tag that you create.
        :param str value: The value that corresponds to the key.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name assigned to the tag that you create.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value that corresponds to the key.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class WorkflowStep(dict):
    """
    The basic building block of a workflow.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "copyStepDetails":
            suggest = "copy_step_details"
        elif key == "customStepDetails":
            suggest = "custom_step_details"
        elif key == "deleteStepDetails":
            suggest = "delete_step_details"
        elif key == "tagStepDetails":
            suggest = "tag_step_details"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkflowStep. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkflowStep.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkflowStep.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 copy_step_details: Optional['outputs.WorkflowStepCopyStepDetailsProperties'] = None,
                 custom_step_details: Optional['outputs.WorkflowStepCustomStepDetailsProperties'] = None,
                 delete_step_details: Optional['outputs.WorkflowStepDeleteStepDetailsProperties'] = None,
                 tag_step_details: Optional['outputs.WorkflowStepTagStepDetailsProperties'] = None,
                 type: Optional['WorkflowStepType'] = None):
        """
        The basic building block of a workflow.
        :param 'WorkflowStepCopyStepDetailsProperties' copy_step_details: Details for a step that performs a file copy.
        :param 'WorkflowStepCustomStepDetailsProperties' custom_step_details: Details for a step that invokes a lambda function.
        :param 'WorkflowStepDeleteStepDetailsProperties' delete_step_details: Details for a step that deletes the file.
        :param 'WorkflowStepTagStepDetailsProperties' tag_step_details: Details for a step that creates one or more tags.
        """
        if copy_step_details is not None:
            pulumi.set(__self__, "copy_step_details", copy_step_details)
        if custom_step_details is not None:
            pulumi.set(__self__, "custom_step_details", custom_step_details)
        if delete_step_details is not None:
            pulumi.set(__self__, "delete_step_details", delete_step_details)
        if tag_step_details is not None:
            pulumi.set(__self__, "tag_step_details", tag_step_details)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="copyStepDetails")
    def copy_step_details(self) -> Optional['outputs.WorkflowStepCopyStepDetailsProperties']:
        """
        Details for a step that performs a file copy.
        """
        return pulumi.get(self, "copy_step_details")

    @property
    @pulumi.getter(name="customStepDetails")
    def custom_step_details(self) -> Optional['outputs.WorkflowStepCustomStepDetailsProperties']:
        """
        Details for a step that invokes a lambda function.
        """
        return pulumi.get(self, "custom_step_details")

    @property
    @pulumi.getter(name="deleteStepDetails")
    def delete_step_details(self) -> Optional['outputs.WorkflowStepDeleteStepDetailsProperties']:
        """
        Details for a step that deletes the file.
        """
        return pulumi.get(self, "delete_step_details")

    @property
    @pulumi.getter(name="tagStepDetails")
    def tag_step_details(self) -> Optional['outputs.WorkflowStepTagStepDetailsProperties']:
        """
        Details for a step that creates one or more tags.
        """
        return pulumi.get(self, "tag_step_details")

    @property
    @pulumi.getter
    def type(self) -> Optional['WorkflowStepType']:
        return pulumi.get(self, "type")


@pulumi.output_type
class WorkflowStepCopyStepDetailsProperties(dict):
    """
    Details for a step that performs a file copy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationFileLocation":
            suggest = "destination_file_location"
        elif key == "overwriteExisting":
            suggest = "overwrite_existing"
        elif key == "sourceFileLocation":
            suggest = "source_file_location"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkflowStepCopyStepDetailsProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkflowStepCopyStepDetailsProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkflowStepCopyStepDetailsProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination_file_location: Optional['outputs.WorkflowInputFileLocation'] = None,
                 name: Optional[str] = None,
                 overwrite_existing: Optional['WorkflowStepCopyStepDetailsPropertiesOverwriteExisting'] = None,
                 source_file_location: Optional[str] = None):
        """
        Details for a step that performs a file copy.
        :param str name: The name of the step, used as an identifier.
        :param 'WorkflowStepCopyStepDetailsPropertiesOverwriteExisting' overwrite_existing: A flag that indicates whether or not to overwrite an existing file of the same name. The default is FALSE.
        :param str source_file_location: Specifies which file to use as input to the workflow step.
        """
        if destination_file_location is not None:
            pulumi.set(__self__, "destination_file_location", destination_file_location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if overwrite_existing is not None:
            pulumi.set(__self__, "overwrite_existing", overwrite_existing)
        if source_file_location is not None:
            pulumi.set(__self__, "source_file_location", source_file_location)

    @property
    @pulumi.getter(name="destinationFileLocation")
    def destination_file_location(self) -> Optional['outputs.WorkflowInputFileLocation']:
        return pulumi.get(self, "destination_file_location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the step, used as an identifier.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="overwriteExisting")
    def overwrite_existing(self) -> Optional['WorkflowStepCopyStepDetailsPropertiesOverwriteExisting']:
        """
        A flag that indicates whether or not to overwrite an existing file of the same name. The default is FALSE.
        """
        return pulumi.get(self, "overwrite_existing")

    @property
    @pulumi.getter(name="sourceFileLocation")
    def source_file_location(self) -> Optional[str]:
        """
        Specifies which file to use as input to the workflow step.
        """
        return pulumi.get(self, "source_file_location")


@pulumi.output_type
class WorkflowStepCustomStepDetailsProperties(dict):
    """
    Details for a step that invokes a lambda function.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sourceFileLocation":
            suggest = "source_file_location"
        elif key == "timeoutSeconds":
            suggest = "timeout_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkflowStepCustomStepDetailsProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkflowStepCustomStepDetailsProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkflowStepCustomStepDetailsProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: Optional[str] = None,
                 source_file_location: Optional[str] = None,
                 target: Optional[str] = None,
                 timeout_seconds: Optional[int] = None):
        """
        Details for a step that invokes a lambda function.
        :param str name: The name of the step, used as an identifier.
        :param str source_file_location: Specifies which file to use as input to the workflow step.
        :param str target: The ARN for the lambda function that is being called.
        :param int timeout_seconds: Timeout, in seconds, for the step.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if source_file_location is not None:
            pulumi.set(__self__, "source_file_location", source_file_location)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if timeout_seconds is not None:
            pulumi.set(__self__, "timeout_seconds", timeout_seconds)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the step, used as an identifier.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sourceFileLocation")
    def source_file_location(self) -> Optional[str]:
        """
        Specifies which file to use as input to the workflow step.
        """
        return pulumi.get(self, "source_file_location")

    @property
    @pulumi.getter
    def target(self) -> Optional[str]:
        """
        The ARN for the lambda function that is being called.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter(name="timeoutSeconds")
    def timeout_seconds(self) -> Optional[int]:
        """
        Timeout, in seconds, for the step.
        """
        return pulumi.get(self, "timeout_seconds")


@pulumi.output_type
class WorkflowStepDeleteStepDetailsProperties(dict):
    """
    Details for a step that deletes the file.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sourceFileLocation":
            suggest = "source_file_location"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkflowStepDeleteStepDetailsProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkflowStepDeleteStepDetailsProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkflowStepDeleteStepDetailsProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: Optional[str] = None,
                 source_file_location: Optional[str] = None):
        """
        Details for a step that deletes the file.
        :param str name: The name of the step, used as an identifier.
        :param str source_file_location: Specifies which file to use as input to the workflow step.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if source_file_location is not None:
            pulumi.set(__self__, "source_file_location", source_file_location)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the step, used as an identifier.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sourceFileLocation")
    def source_file_location(self) -> Optional[str]:
        """
        Specifies which file to use as input to the workflow step.
        """
        return pulumi.get(self, "source_file_location")


@pulumi.output_type
class WorkflowStepTagStepDetailsProperties(dict):
    """
    Details for a step that creates one or more tags.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sourceFileLocation":
            suggest = "source_file_location"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkflowStepTagStepDetailsProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkflowStepTagStepDetailsProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkflowStepTagStepDetailsProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: Optional[str] = None,
                 source_file_location: Optional[str] = None,
                 tags: Optional[Sequence['outputs.WorkflowS3Tag']] = None):
        """
        Details for a step that creates one or more tags.
        :param str name: The name of the step, used as an identifier.
        :param str source_file_location: Specifies which file to use as input to the workflow step.
        :param Sequence['WorkflowS3Tag'] tags: Array that contains from 1 to 10 key/value pairs.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if source_file_location is not None:
            pulumi.set(__self__, "source_file_location", source_file_location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the step, used as an identifier.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sourceFileLocation")
    def source_file_location(self) -> Optional[str]:
        """
        Specifies which file to use as input to the workflow step.
        """
        return pulumi.get(self, "source_file_location")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.WorkflowS3Tag']]:
        """
        Array that contains from 1 to 10 key/value pairs.
        """
        return pulumi.get(self, "tags")


@pulumi.output_type
class WorkflowTag(dict):
    """
    Creates a key-value pair for a specific resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        Creates a key-value pair for a specific resource.
        :param str key: The name assigned to the tag that you create.
        :param str value: Contains one or more values that you assigned to the key name you create.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name assigned to the tag that you create.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Contains one or more values that you assigned to the key name you create.
        """
        return pulumi.get(self, "value")


