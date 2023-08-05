# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ProjectArtifactsArgs',
    'ProjectBatchRestrictionsArgs',
    'ProjectBuildBatchConfigArgs',
    'ProjectBuildStatusConfigArgs',
    'ProjectCacheArgs',
    'ProjectCloudWatchLogsConfigArgs',
    'ProjectEnvironmentVariableArgs',
    'ProjectEnvironmentArgs',
    'ProjectFileSystemLocationArgs',
    'ProjectFilterGroupArgs',
    'ProjectGitSubmodulesConfigArgs',
    'ProjectLogsConfigArgs',
    'ProjectRegistryCredentialArgs',
    'ProjectS3LogsConfigArgs',
    'ProjectSourceAuthArgs',
    'ProjectSourceVersionArgs',
    'ProjectSourceArgs',
    'ProjectTagArgs',
    'ProjectTriggersArgs',
    'ProjectVpcConfigArgs',
    'ReportGroupReportExportConfigArgs',
    'ReportGroupS3ReportExportConfigArgs',
    'ReportGroupTagArgs',
]

@pulumi.input_type
class ProjectArtifactsArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 artifact_identifier: Optional[pulumi.Input[str]] = None,
                 encryption_disabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_type: Optional[pulumi.Input[str]] = None,
                 override_artifact_name: Optional[pulumi.Input[bool]] = None,
                 packaging: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "type", type)
        if artifact_identifier is not None:
            pulumi.set(__self__, "artifact_identifier", artifact_identifier)
        if encryption_disabled is not None:
            pulumi.set(__self__, "encryption_disabled", encryption_disabled)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace_type is not None:
            pulumi.set(__self__, "namespace_type", namespace_type)
        if override_artifact_name is not None:
            pulumi.set(__self__, "override_artifact_name", override_artifact_name)
        if packaging is not None:
            pulumi.set(__self__, "packaging", packaging)
        if path is not None:
            pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="artifactIdentifier")
    def artifact_identifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "artifact_identifier")

    @artifact_identifier.setter
    def artifact_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_identifier", value)

    @property
    @pulumi.getter(name="encryptionDisabled")
    def encryption_disabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "encryption_disabled")

    @encryption_disabled.setter
    def encryption_disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encryption_disabled", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namespaceType")
    def namespace_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "namespace_type")

    @namespace_type.setter
    def namespace_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_type", value)

    @property
    @pulumi.getter(name="overrideArtifactName")
    def override_artifact_name(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "override_artifact_name")

    @override_artifact_name.setter
    def override_artifact_name(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "override_artifact_name", value)

    @property
    @pulumi.getter
    def packaging(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "packaging")

    @packaging.setter
    def packaging(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "packaging", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)


@pulumi.input_type
class ProjectBatchRestrictionsArgs:
    def __init__(__self__, *,
                 compute_types_allowed: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 maximum_builds_allowed: Optional[pulumi.Input[int]] = None):
        if compute_types_allowed is not None:
            pulumi.set(__self__, "compute_types_allowed", compute_types_allowed)
        if maximum_builds_allowed is not None:
            pulumi.set(__self__, "maximum_builds_allowed", maximum_builds_allowed)

    @property
    @pulumi.getter(name="computeTypesAllowed")
    def compute_types_allowed(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "compute_types_allowed")

    @compute_types_allowed.setter
    def compute_types_allowed(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "compute_types_allowed", value)

    @property
    @pulumi.getter(name="maximumBuildsAllowed")
    def maximum_builds_allowed(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "maximum_builds_allowed")

    @maximum_builds_allowed.setter
    def maximum_builds_allowed(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "maximum_builds_allowed", value)


@pulumi.input_type
class ProjectBuildBatchConfigArgs:
    def __init__(__self__, *,
                 batch_report_mode: Optional[pulumi.Input[str]] = None,
                 combine_artifacts: Optional[pulumi.Input[bool]] = None,
                 restrictions: Optional[pulumi.Input['ProjectBatchRestrictionsArgs']] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 timeout_in_mins: Optional[pulumi.Input[int]] = None):
        if batch_report_mode is not None:
            pulumi.set(__self__, "batch_report_mode", batch_report_mode)
        if combine_artifacts is not None:
            pulumi.set(__self__, "combine_artifacts", combine_artifacts)
        if restrictions is not None:
            pulumi.set(__self__, "restrictions", restrictions)
        if service_role is not None:
            pulumi.set(__self__, "service_role", service_role)
        if timeout_in_mins is not None:
            pulumi.set(__self__, "timeout_in_mins", timeout_in_mins)

    @property
    @pulumi.getter(name="batchReportMode")
    def batch_report_mode(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "batch_report_mode")

    @batch_report_mode.setter
    def batch_report_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "batch_report_mode", value)

    @property
    @pulumi.getter(name="combineArtifacts")
    def combine_artifacts(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "combine_artifacts")

    @combine_artifacts.setter
    def combine_artifacts(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "combine_artifacts", value)

    @property
    @pulumi.getter
    def restrictions(self) -> Optional[pulumi.Input['ProjectBatchRestrictionsArgs']]:
        return pulumi.get(self, "restrictions")

    @restrictions.setter
    def restrictions(self, value: Optional[pulumi.Input['ProjectBatchRestrictionsArgs']]):
        pulumi.set(self, "restrictions", value)

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "service_role")

    @service_role.setter
    def service_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_role", value)

    @property
    @pulumi.getter(name="timeoutInMins")
    def timeout_in_mins(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "timeout_in_mins")

    @timeout_in_mins.setter
    def timeout_in_mins(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_in_mins", value)


@pulumi.input_type
class ProjectBuildStatusConfigArgs:
    def __init__(__self__, *,
                 context: Optional[pulumi.Input[str]] = None,
                 target_url: Optional[pulumi.Input[str]] = None):
        if context is not None:
            pulumi.set(__self__, "context", context)
        if target_url is not None:
            pulumi.set(__self__, "target_url", target_url)

    @property
    @pulumi.getter
    def context(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "context")

    @context.setter
    def context(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "context", value)

    @property
    @pulumi.getter(name="targetUrl")
    def target_url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "target_url")

    @target_url.setter
    def target_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_url", value)


@pulumi.input_type
class ProjectCacheArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 modes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        pulumi.set(__self__, "type", type)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if modes is not None:
            pulumi.set(__self__, "modes", modes)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def modes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "modes")

    @modes.setter
    def modes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "modes", value)


@pulumi.input_type
class ProjectCloudWatchLogsConfigArgs:
    def __init__(__self__, *,
                 status: pulumi.Input[str],
                 group_name: Optional[pulumi.Input[str]] = None,
                 stream_name: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "status", status)
        if group_name is not None:
            pulumi.set(__self__, "group_name", group_name)
        if stream_name is not None:
            pulumi.set(__self__, "stream_name", stream_name)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input[str]:
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[str]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter(name="streamName")
    def stream_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "stream_name")

    @stream_name.setter
    def stream_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_name", value)


@pulumi.input_type
class ProjectEnvironmentVariableArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str],
                 type: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ProjectEnvironmentArgs:
    def __init__(__self__, *,
                 compute_type: pulumi.Input[str],
                 image: pulumi.Input[str],
                 type: pulumi.Input[str],
                 certificate: Optional[pulumi.Input[str]] = None,
                 environment_variables: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectEnvironmentVariableArgs']]]] = None,
                 image_pull_credentials_type: Optional[pulumi.Input[str]] = None,
                 privileged_mode: Optional[pulumi.Input[bool]] = None,
                 registry_credential: Optional[pulumi.Input['ProjectRegistryCredentialArgs']] = None):
        pulumi.set(__self__, "compute_type", compute_type)
        pulumi.set(__self__, "image", image)
        pulumi.set(__self__, "type", type)
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if image_pull_credentials_type is not None:
            pulumi.set(__self__, "image_pull_credentials_type", image_pull_credentials_type)
        if privileged_mode is not None:
            pulumi.set(__self__, "privileged_mode", privileged_mode)
        if registry_credential is not None:
            pulumi.set(__self__, "registry_credential", registry_credential)

    @property
    @pulumi.getter(name="computeType")
    def compute_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "compute_type")

    @compute_type.setter
    def compute_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "compute_type", value)

    @property
    @pulumi.getter
    def image(self) -> pulumi.Input[str]:
        return pulumi.get(self, "image")

    @image.setter
    def image(self, value: pulumi.Input[str]):
        pulumi.set(self, "image", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ProjectEnvironmentVariableArgs']]]]:
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectEnvironmentVariableArgs']]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter(name="imagePullCredentialsType")
    def image_pull_credentials_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "image_pull_credentials_type")

    @image_pull_credentials_type.setter
    def image_pull_credentials_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_pull_credentials_type", value)

    @property
    @pulumi.getter(name="privilegedMode")
    def privileged_mode(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "privileged_mode")

    @privileged_mode.setter
    def privileged_mode(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "privileged_mode", value)

    @property
    @pulumi.getter(name="registryCredential")
    def registry_credential(self) -> Optional[pulumi.Input['ProjectRegistryCredentialArgs']]:
        return pulumi.get(self, "registry_credential")

    @registry_credential.setter
    def registry_credential(self, value: Optional[pulumi.Input['ProjectRegistryCredentialArgs']]):
        pulumi.set(self, "registry_credential", value)


@pulumi.input_type
class ProjectFileSystemLocationArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 location: pulumi.Input[str],
                 mount_point: pulumi.Input[str],
                 type: pulumi.Input[str],
                 mount_options: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "mount_point", mount_point)
        pulumi.set(__self__, "type", type)
        if mount_options is not None:
            pulumi.set(__self__, "mount_options", mount_options)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mountPoint")
    def mount_point(self) -> pulumi.Input[str]:
        return pulumi.get(self, "mount_point")

    @mount_point.setter
    def mount_point(self, value: pulumi.Input[str]):
        pulumi.set(self, "mount_point", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="mountOptions")
    def mount_options(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "mount_options")

    @mount_options.setter
    def mount_options(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mount_options", value)


@pulumi.input_type
class ProjectFilterGroupArgs:
    def __init__(__self__):
        pass


@pulumi.input_type
class ProjectGitSubmodulesConfigArgs:
    def __init__(__self__, *,
                 fetch_submodules: pulumi.Input[bool]):
        pulumi.set(__self__, "fetch_submodules", fetch_submodules)

    @property
    @pulumi.getter(name="fetchSubmodules")
    def fetch_submodules(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "fetch_submodules")

    @fetch_submodules.setter
    def fetch_submodules(self, value: pulumi.Input[bool]):
        pulumi.set(self, "fetch_submodules", value)


@pulumi.input_type
class ProjectLogsConfigArgs:
    def __init__(__self__, *,
                 cloud_watch_logs: Optional[pulumi.Input['ProjectCloudWatchLogsConfigArgs']] = None,
                 s3_logs: Optional[pulumi.Input['ProjectS3LogsConfigArgs']] = None):
        if cloud_watch_logs is not None:
            pulumi.set(__self__, "cloud_watch_logs", cloud_watch_logs)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter(name="cloudWatchLogs")
    def cloud_watch_logs(self) -> Optional[pulumi.Input['ProjectCloudWatchLogsConfigArgs']]:
        return pulumi.get(self, "cloud_watch_logs")

    @cloud_watch_logs.setter
    def cloud_watch_logs(self, value: Optional[pulumi.Input['ProjectCloudWatchLogsConfigArgs']]):
        pulumi.set(self, "cloud_watch_logs", value)

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional[pulumi.Input['ProjectS3LogsConfigArgs']]:
        return pulumi.get(self, "s3_logs")

    @s3_logs.setter
    def s3_logs(self, value: Optional[pulumi.Input['ProjectS3LogsConfigArgs']]):
        pulumi.set(self, "s3_logs", value)


@pulumi.input_type
class ProjectRegistryCredentialArgs:
    def __init__(__self__, *,
                 credential: pulumi.Input[str],
                 credential_provider: pulumi.Input[str]):
        pulumi.set(__self__, "credential", credential)
        pulumi.set(__self__, "credential_provider", credential_provider)

    @property
    @pulumi.getter
    def credential(self) -> pulumi.Input[str]:
        return pulumi.get(self, "credential")

    @credential.setter
    def credential(self, value: pulumi.Input[str]):
        pulumi.set(self, "credential", value)

    @property
    @pulumi.getter(name="credentialProvider")
    def credential_provider(self) -> pulumi.Input[str]:
        return pulumi.get(self, "credential_provider")

    @credential_provider.setter
    def credential_provider(self, value: pulumi.Input[str]):
        pulumi.set(self, "credential_provider", value)


@pulumi.input_type
class ProjectS3LogsConfigArgs:
    def __init__(__self__, *,
                 status: pulumi.Input[str],
                 encryption_disabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "status", status)
        if encryption_disabled is not None:
            pulumi.set(__self__, "encryption_disabled", encryption_disabled)
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input[str]:
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[str]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="encryptionDisabled")
    def encryption_disabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "encryption_disabled")

    @encryption_disabled.setter
    def encryption_disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encryption_disabled", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)


@pulumi.input_type
class ProjectSourceAuthArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 resource: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "type", type)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def resource(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource")

    @resource.setter
    def resource(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource", value)


@pulumi.input_type
class ProjectSourceVersionArgs:
    def __init__(__self__, *,
                 source_identifier: pulumi.Input[str],
                 source_version: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "source_identifier", source_identifier)
        if source_version is not None:
            pulumi.set(__self__, "source_version", source_version)

    @property
    @pulumi.getter(name="sourceIdentifier")
    def source_identifier(self) -> pulumi.Input[str]:
        return pulumi.get(self, "source_identifier")

    @source_identifier.setter
    def source_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_identifier", value)

    @property
    @pulumi.getter(name="sourceVersion")
    def source_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_version")

    @source_version.setter
    def source_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_version", value)


@pulumi.input_type
class ProjectSourceArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 auth: Optional[pulumi.Input['ProjectSourceAuthArgs']] = None,
                 build_spec: Optional[pulumi.Input[str]] = None,
                 build_status_config: Optional[pulumi.Input['ProjectBuildStatusConfigArgs']] = None,
                 git_clone_depth: Optional[pulumi.Input[int]] = None,
                 git_submodules_config: Optional[pulumi.Input['ProjectGitSubmodulesConfigArgs']] = None,
                 insecure_ssl: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 report_build_status: Optional[pulumi.Input[bool]] = None,
                 source_identifier: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "type", type)
        if auth is not None:
            pulumi.set(__self__, "auth", auth)
        if build_spec is not None:
            pulumi.set(__self__, "build_spec", build_spec)
        if build_status_config is not None:
            pulumi.set(__self__, "build_status_config", build_status_config)
        if git_clone_depth is not None:
            pulumi.set(__self__, "git_clone_depth", git_clone_depth)
        if git_submodules_config is not None:
            pulumi.set(__self__, "git_submodules_config", git_submodules_config)
        if insecure_ssl is not None:
            pulumi.set(__self__, "insecure_ssl", insecure_ssl)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if report_build_status is not None:
            pulumi.set(__self__, "report_build_status", report_build_status)
        if source_identifier is not None:
            pulumi.set(__self__, "source_identifier", source_identifier)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def auth(self) -> Optional[pulumi.Input['ProjectSourceAuthArgs']]:
        return pulumi.get(self, "auth")

    @auth.setter
    def auth(self, value: Optional[pulumi.Input['ProjectSourceAuthArgs']]):
        pulumi.set(self, "auth", value)

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "build_spec")

    @build_spec.setter
    def build_spec(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "build_spec", value)

    @property
    @pulumi.getter(name="buildStatusConfig")
    def build_status_config(self) -> Optional[pulumi.Input['ProjectBuildStatusConfigArgs']]:
        return pulumi.get(self, "build_status_config")

    @build_status_config.setter
    def build_status_config(self, value: Optional[pulumi.Input['ProjectBuildStatusConfigArgs']]):
        pulumi.set(self, "build_status_config", value)

    @property
    @pulumi.getter(name="gitCloneDepth")
    def git_clone_depth(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "git_clone_depth")

    @git_clone_depth.setter
    def git_clone_depth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "git_clone_depth", value)

    @property
    @pulumi.getter(name="gitSubmodulesConfig")
    def git_submodules_config(self) -> Optional[pulumi.Input['ProjectGitSubmodulesConfigArgs']]:
        return pulumi.get(self, "git_submodules_config")

    @git_submodules_config.setter
    def git_submodules_config(self, value: Optional[pulumi.Input['ProjectGitSubmodulesConfigArgs']]):
        pulumi.set(self, "git_submodules_config", value)

    @property
    @pulumi.getter(name="insecureSsl")
    def insecure_ssl(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "insecure_ssl")

    @insecure_ssl.setter
    def insecure_ssl(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "insecure_ssl", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="reportBuildStatus")
    def report_build_status(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "report_build_status")

    @report_build_status.setter
    def report_build_status(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "report_build_status", value)

    @property
    @pulumi.getter(name="sourceIdentifier")
    def source_identifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_identifier")

    @source_identifier.setter
    def source_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_identifier", value)


@pulumi.input_type
class ProjectTagArgs:
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


@pulumi.input_type
class ProjectTriggersArgs:
    def __init__(__self__, *,
                 build_type: Optional[pulumi.Input[str]] = None,
                 filter_groups: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectFilterGroupArgs']]]] = None,
                 webhook: Optional[pulumi.Input[bool]] = None):
        if build_type is not None:
            pulumi.set(__self__, "build_type", build_type)
        if filter_groups is not None:
            pulumi.set(__self__, "filter_groups", filter_groups)
        if webhook is not None:
            pulumi.set(__self__, "webhook", webhook)

    @property
    @pulumi.getter(name="buildType")
    def build_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "build_type")

    @build_type.setter
    def build_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "build_type", value)

    @property
    @pulumi.getter(name="filterGroups")
    def filter_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ProjectFilterGroupArgs']]]]:
        return pulumi.get(self, "filter_groups")

    @filter_groups.setter
    def filter_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectFilterGroupArgs']]]]):
        pulumi.set(self, "filter_groups", value)

    @property
    @pulumi.getter
    def webhook(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "webhook")

    @webhook.setter
    def webhook(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "webhook", value)


@pulumi.input_type
class ProjectVpcConfigArgs:
    def __init__(__self__, *,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnets is not None:
            pulumi.set(__self__, "subnets", subnets)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter
    def subnets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "subnets")

    @subnets.setter
    def subnets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnets", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


@pulumi.input_type
class ReportGroupReportExportConfigArgs:
    def __init__(__self__, *,
                 export_config_type: pulumi.Input[str],
                 s3_destination: Optional[pulumi.Input['ReportGroupS3ReportExportConfigArgs']] = None):
        pulumi.set(__self__, "export_config_type", export_config_type)
        if s3_destination is not None:
            pulumi.set(__self__, "s3_destination", s3_destination)

    @property
    @pulumi.getter(name="exportConfigType")
    def export_config_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "export_config_type")

    @export_config_type.setter
    def export_config_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "export_config_type", value)

    @property
    @pulumi.getter(name="s3Destination")
    def s3_destination(self) -> Optional[pulumi.Input['ReportGroupS3ReportExportConfigArgs']]:
        return pulumi.get(self, "s3_destination")

    @s3_destination.setter
    def s3_destination(self, value: Optional[pulumi.Input['ReportGroupS3ReportExportConfigArgs']]):
        pulumi.set(self, "s3_destination", value)


@pulumi.input_type
class ReportGroupS3ReportExportConfigArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 bucket_owner: Optional[pulumi.Input[str]] = None,
                 encryption_disabled: Optional[pulumi.Input[bool]] = None,
                 encryption_key: Optional[pulumi.Input[str]] = None,
                 packaging: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "bucket", bucket)
        if bucket_owner is not None:
            pulumi.set(__self__, "bucket_owner", bucket_owner)
        if encryption_disabled is not None:
            pulumi.set(__self__, "encryption_disabled", encryption_disabled)
        if encryption_key is not None:
            pulumi.set(__self__, "encryption_key", encryption_key)
        if packaging is not None:
            pulumi.set(__self__, "packaging", packaging)
        if path is not None:
            pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="bucketOwner")
    def bucket_owner(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket_owner")

    @bucket_owner.setter
    def bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_owner", value)

    @property
    @pulumi.getter(name="encryptionDisabled")
    def encryption_disabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "encryption_disabled")

    @encryption_disabled.setter
    def encryption_disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encryption_disabled", value)

    @property
    @pulumi.getter(name="encryptionKey")
    def encryption_key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "encryption_key")

    @encryption_key.setter
    def encryption_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encryption_key", value)

    @property
    @pulumi.getter
    def packaging(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "packaging")

    @packaging.setter
    def packaging(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "packaging", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)


@pulumi.input_type
class ReportGroupTagArgs:
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


