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
    'LaunchProfileStreamConfigurationSessionStorageArgs',
    'LaunchProfileStreamConfigurationArgs',
    'LaunchProfileStreamingSessionStorageRootArgs',
    'LaunchProfileTagsArgs',
    'StreamingImageTagsArgs',
    'StudioComponentActiveDirectoryComputerAttributeArgs',
    'StudioComponentActiveDirectoryConfigurationArgs',
    'StudioComponentComputeFarmConfigurationArgs',
    'StudioComponentConfigurationArgs',
    'StudioComponentInitializationScriptArgs',
    'StudioComponentLicenseServiceConfigurationArgs',
    'StudioComponentScriptParameterKeyValueArgs',
    'StudioComponentSharedFileSystemConfigurationArgs',
    'StudioComponentTagsArgs',
    'StudioEncryptionConfigurationArgs',
    'StudioTagsArgs',
]

@pulumi.input_type
class LaunchProfileStreamConfigurationSessionStorageArgs:
    def __init__(__self__, *,
                 mode: Optional[pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingSessionStorageMode']]]] = None,
                 root: Optional[pulumi.Input['LaunchProfileStreamingSessionStorageRootArgs']] = None):
        """
        <p>The configuration for a streaming session’s upload storage.</p>
        :param pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingSessionStorageMode']]] mode: <p>Allows artists to upload files to their workstations. The only valid option is
                               <code>UPLOAD</code>.</p>
        """
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if root is not None:
            pulumi.set(__self__, "root", root)

    @property
    @pulumi.getter
    def mode(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingSessionStorageMode']]]]:
        """
        <p>Allows artists to upload files to their workstations. The only valid option is
                        <code>UPLOAD</code>.</p>
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingSessionStorageMode']]]]):
        pulumi.set(self, "mode", value)

    @property
    @pulumi.getter
    def root(self) -> Optional[pulumi.Input['LaunchProfileStreamingSessionStorageRootArgs']]:
        return pulumi.get(self, "root")

    @root.setter
    def root(self, value: Optional[pulumi.Input['LaunchProfileStreamingSessionStorageRootArgs']]):
        pulumi.set(self, "root", value)


@pulumi.input_type
class LaunchProfileStreamConfigurationArgs:
    def __init__(__self__, *,
                 clipboard_mode: pulumi.Input['LaunchProfileStreamingClipboardMode'],
                 ec2_instance_types: pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingInstanceType']]],
                 streaming_image_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 max_session_length_in_minutes: Optional[pulumi.Input[float]] = None,
                 max_stopped_session_length_in_minutes: Optional[pulumi.Input[float]] = None,
                 session_storage: Optional[pulumi.Input['LaunchProfileStreamConfigurationSessionStorageArgs']] = None):
        """
        <p>A configuration for a streaming session.</p>
        :param pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingInstanceType']]] ec2_instance_types: <p>The EC2 instance types that users can select from when launching a streaming session
                           with this launch profile.</p>
        :param pulumi.Input[Sequence[pulumi.Input[str]]] streaming_image_ids: <p>The streaming images that users can select from when launching a streaming session
                           with this launch profile.</p>
        :param pulumi.Input[float] max_session_length_in_minutes: <p>The length of time, in minutes, that a streaming session can be active before it is
                           stopped or terminated. After this point, Nimble Studio automatically terminates or
                           stops the session. The default length of time is 690 minutes, and the maximum length of
                           time is 30 days.</p>
        :param pulumi.Input[float] max_stopped_session_length_in_minutes: <p>Integer that determines if you can start and stop your sessions and how long a session
                           can stay in the STOPPED state. The default value is 0. The maximum value is 5760.</p>
                       <p>If the value is missing or set to 0, your sessions can’t be stopped. If you then call
                           StopStreamingSession, the session fails. If the time that a session stays in the READY
                           state exceeds the maxSessionLengthInMinutes value, the session will automatically be
                           terminated by AWS (instead of stopped).</p>
                       <p>If the value is set to a positive number, the session can be stopped. You can call
                           StopStreamingSession to stop sessions in the READY state. If the time that a session
                           stays in the READY state exceeds the maxSessionLengthInMinutes value, the session will
                           automatically be stopped by AWS (instead of terminated).</p>
        """
        pulumi.set(__self__, "clipboard_mode", clipboard_mode)
        pulumi.set(__self__, "ec2_instance_types", ec2_instance_types)
        pulumi.set(__self__, "streaming_image_ids", streaming_image_ids)
        if max_session_length_in_minutes is not None:
            pulumi.set(__self__, "max_session_length_in_minutes", max_session_length_in_minutes)
        if max_stopped_session_length_in_minutes is not None:
            pulumi.set(__self__, "max_stopped_session_length_in_minutes", max_stopped_session_length_in_minutes)
        if session_storage is not None:
            pulumi.set(__self__, "session_storage", session_storage)

    @property
    @pulumi.getter(name="clipboardMode")
    def clipboard_mode(self) -> pulumi.Input['LaunchProfileStreamingClipboardMode']:
        return pulumi.get(self, "clipboard_mode")

    @clipboard_mode.setter
    def clipboard_mode(self, value: pulumi.Input['LaunchProfileStreamingClipboardMode']):
        pulumi.set(self, "clipboard_mode", value)

    @property
    @pulumi.getter(name="ec2InstanceTypes")
    def ec2_instance_types(self) -> pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingInstanceType']]]:
        """
        <p>The EC2 instance types that users can select from when launching a streaming session
                    with this launch profile.</p>
        """
        return pulumi.get(self, "ec2_instance_types")

    @ec2_instance_types.setter
    def ec2_instance_types(self, value: pulumi.Input[Sequence[pulumi.Input['LaunchProfileStreamingInstanceType']]]):
        pulumi.set(self, "ec2_instance_types", value)

    @property
    @pulumi.getter(name="streamingImageIds")
    def streaming_image_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        <p>The streaming images that users can select from when launching a streaming session
                    with this launch profile.</p>
        """
        return pulumi.get(self, "streaming_image_ids")

    @streaming_image_ids.setter
    def streaming_image_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "streaming_image_ids", value)

    @property
    @pulumi.getter(name="maxSessionLengthInMinutes")
    def max_session_length_in_minutes(self) -> Optional[pulumi.Input[float]]:
        """
        <p>The length of time, in minutes, that a streaming session can be active before it is
                    stopped or terminated. After this point, Nimble Studio automatically terminates or
                    stops the session. The default length of time is 690 minutes, and the maximum length of
                    time is 30 days.</p>
        """
        return pulumi.get(self, "max_session_length_in_minutes")

    @max_session_length_in_minutes.setter
    def max_session_length_in_minutes(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_session_length_in_minutes", value)

    @property
    @pulumi.getter(name="maxStoppedSessionLengthInMinutes")
    def max_stopped_session_length_in_minutes(self) -> Optional[pulumi.Input[float]]:
        """
        <p>Integer that determines if you can start and stop your sessions and how long a session
                    can stay in the STOPPED state. The default value is 0. The maximum value is 5760.</p>
                <p>If the value is missing or set to 0, your sessions can’t be stopped. If you then call
                    StopStreamingSession, the session fails. If the time that a session stays in the READY
                    state exceeds the maxSessionLengthInMinutes value, the session will automatically be
                    terminated by AWS (instead of stopped).</p>
                <p>If the value is set to a positive number, the session can be stopped. You can call
                    StopStreamingSession to stop sessions in the READY state. If the time that a session
                    stays in the READY state exceeds the maxSessionLengthInMinutes value, the session will
                    automatically be stopped by AWS (instead of terminated).</p>
        """
        return pulumi.get(self, "max_stopped_session_length_in_minutes")

    @max_stopped_session_length_in_minutes.setter
    def max_stopped_session_length_in_minutes(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_stopped_session_length_in_minutes", value)

    @property
    @pulumi.getter(name="sessionStorage")
    def session_storage(self) -> Optional[pulumi.Input['LaunchProfileStreamConfigurationSessionStorageArgs']]:
        return pulumi.get(self, "session_storage")

    @session_storage.setter
    def session_storage(self, value: Optional[pulumi.Input['LaunchProfileStreamConfigurationSessionStorageArgs']]):
        pulumi.set(self, "session_storage", value)


@pulumi.input_type
class LaunchProfileStreamingSessionStorageRootArgs:
    def __init__(__self__, *,
                 linux: Optional[pulumi.Input[str]] = None,
                 windows: Optional[pulumi.Input[str]] = None):
        """
        <p>The upload storage root location (folder) on streaming workstations where files are
                    uploaded.</p>
        :param pulumi.Input[str] linux: <p>The folder path in Linux workstations where files are uploaded.</p>
        :param pulumi.Input[str] windows: <p>The folder path in Windows workstations where files are uploaded.</p>
        """
        if linux is not None:
            pulumi.set(__self__, "linux", linux)
        if windows is not None:
            pulumi.set(__self__, "windows", windows)

    @property
    @pulumi.getter
    def linux(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The folder path in Linux workstations where files are uploaded.</p>
        """
        return pulumi.get(self, "linux")

    @linux.setter
    def linux(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "linux", value)

    @property
    @pulumi.getter
    def windows(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The folder path in Windows workstations where files are uploaded.</p>
        """
        return pulumi.get(self, "windows")

    @windows.setter
    def windows(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "windows", value)


@pulumi.input_type
class LaunchProfileTagsArgs:
    def __init__(__self__):
        pass


@pulumi.input_type
class StreamingImageTagsArgs:
    def __init__(__self__):
        pass


@pulumi.input_type
class StudioComponentActiveDirectoryComputerAttributeArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        <p>An LDAP attribute of an Active Directory computer account, in the form of a name:value pair.</p>
        :param pulumi.Input[str] name: <p>The name for the LDAP attribute.</p>
        :param pulumi.Input[str] value: <p>The value for the LDAP attribute.</p>
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The name for the LDAP attribute.</p>
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The value for the LDAP attribute.</p>
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class StudioComponentActiveDirectoryConfigurationArgs:
    def __init__(__self__, *,
                 computer_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['StudioComponentActiveDirectoryComputerAttributeArgs']]]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 organizational_unit_distinguished_name: Optional[pulumi.Input[str]] = None):
        """
        <p>The configuration for a Microsoft Active Directory (Microsoft AD) studio resource.</p>
        :param pulumi.Input[Sequence[pulumi.Input['StudioComponentActiveDirectoryComputerAttributeArgs']]] computer_attributes: <p>A collection of custom attributes for an Active Directory computer.</p>
        :param pulumi.Input[str] directory_id: <p>The directory ID of the Directory Service for Microsoft Active Directory to access using this studio component.</p>
        :param pulumi.Input[str] organizational_unit_distinguished_name: <p>The distinguished name (DN) and organizational unit (OU) of an Active Directory computer.</p>
        """
        if computer_attributes is not None:
            pulumi.set(__self__, "computer_attributes", computer_attributes)
        if directory_id is not None:
            pulumi.set(__self__, "directory_id", directory_id)
        if organizational_unit_distinguished_name is not None:
            pulumi.set(__self__, "organizational_unit_distinguished_name", organizational_unit_distinguished_name)

    @property
    @pulumi.getter(name="computerAttributes")
    def computer_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StudioComponentActiveDirectoryComputerAttributeArgs']]]]:
        """
        <p>A collection of custom attributes for an Active Directory computer.</p>
        """
        return pulumi.get(self, "computer_attributes")

    @computer_attributes.setter
    def computer_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StudioComponentActiveDirectoryComputerAttributeArgs']]]]):
        pulumi.set(self, "computer_attributes", value)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The directory ID of the Directory Service for Microsoft Active Directory to access using this studio component.</p>
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter(name="organizationalUnitDistinguishedName")
    def organizational_unit_distinguished_name(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The distinguished name (DN) and organizational unit (OU) of an Active Directory computer.</p>
        """
        return pulumi.get(self, "organizational_unit_distinguished_name")

    @organizational_unit_distinguished_name.setter
    def organizational_unit_distinguished_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organizational_unit_distinguished_name", value)


@pulumi.input_type
class StudioComponentComputeFarmConfigurationArgs:
    def __init__(__self__, *,
                 active_directory_user: Optional[pulumi.Input[str]] = None,
                 endpoint: Optional[pulumi.Input[str]] = None):
        """
        <p>The configuration for a render farm that is associated with a studio resource.</p>
        :param pulumi.Input[str] active_directory_user: <p>The name of an Active Directory user that is used on ComputeFarm worker instances.</p>
        :param pulumi.Input[str] endpoint: <p>The endpoint of the ComputeFarm that is accessed by the studio component resource.</p>
        """
        if active_directory_user is not None:
            pulumi.set(__self__, "active_directory_user", active_directory_user)
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)

    @property
    @pulumi.getter(name="activeDirectoryUser")
    def active_directory_user(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The name of an Active Directory user that is used on ComputeFarm worker instances.</p>
        """
        return pulumi.get(self, "active_directory_user")

    @active_directory_user.setter
    def active_directory_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "active_directory_user", value)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The endpoint of the ComputeFarm that is accessed by the studio component resource.</p>
        """
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint", value)


@pulumi.input_type
class StudioComponentConfigurationArgs:
    def __init__(__self__, *,
                 active_directory_configuration: Optional[pulumi.Input['StudioComponentActiveDirectoryConfigurationArgs']] = None,
                 compute_farm_configuration: Optional[pulumi.Input['StudioComponentComputeFarmConfigurationArgs']] = None,
                 license_service_configuration: Optional[pulumi.Input['StudioComponentLicenseServiceConfigurationArgs']] = None,
                 shared_file_system_configuration: Optional[pulumi.Input['StudioComponentSharedFileSystemConfigurationArgs']] = None):
        """
        <p>The configuration of the studio component, based on component type.</p>
        """
        if active_directory_configuration is not None:
            pulumi.set(__self__, "active_directory_configuration", active_directory_configuration)
        if compute_farm_configuration is not None:
            pulumi.set(__self__, "compute_farm_configuration", compute_farm_configuration)
        if license_service_configuration is not None:
            pulumi.set(__self__, "license_service_configuration", license_service_configuration)
        if shared_file_system_configuration is not None:
            pulumi.set(__self__, "shared_file_system_configuration", shared_file_system_configuration)

    @property
    @pulumi.getter(name="activeDirectoryConfiguration")
    def active_directory_configuration(self) -> Optional[pulumi.Input['StudioComponentActiveDirectoryConfigurationArgs']]:
        return pulumi.get(self, "active_directory_configuration")

    @active_directory_configuration.setter
    def active_directory_configuration(self, value: Optional[pulumi.Input['StudioComponentActiveDirectoryConfigurationArgs']]):
        pulumi.set(self, "active_directory_configuration", value)

    @property
    @pulumi.getter(name="computeFarmConfiguration")
    def compute_farm_configuration(self) -> Optional[pulumi.Input['StudioComponentComputeFarmConfigurationArgs']]:
        return pulumi.get(self, "compute_farm_configuration")

    @compute_farm_configuration.setter
    def compute_farm_configuration(self, value: Optional[pulumi.Input['StudioComponentComputeFarmConfigurationArgs']]):
        pulumi.set(self, "compute_farm_configuration", value)

    @property
    @pulumi.getter(name="licenseServiceConfiguration")
    def license_service_configuration(self) -> Optional[pulumi.Input['StudioComponentLicenseServiceConfigurationArgs']]:
        return pulumi.get(self, "license_service_configuration")

    @license_service_configuration.setter
    def license_service_configuration(self, value: Optional[pulumi.Input['StudioComponentLicenseServiceConfigurationArgs']]):
        pulumi.set(self, "license_service_configuration", value)

    @property
    @pulumi.getter(name="sharedFileSystemConfiguration")
    def shared_file_system_configuration(self) -> Optional[pulumi.Input['StudioComponentSharedFileSystemConfigurationArgs']]:
        return pulumi.get(self, "shared_file_system_configuration")

    @shared_file_system_configuration.setter
    def shared_file_system_configuration(self, value: Optional[pulumi.Input['StudioComponentSharedFileSystemConfigurationArgs']]):
        pulumi.set(self, "shared_file_system_configuration", value)


@pulumi.input_type
class StudioComponentInitializationScriptArgs:
    def __init__(__self__, *,
                 launch_profile_protocol_version: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input['StudioComponentLaunchProfilePlatform']] = None,
                 run_context: Optional[pulumi.Input['StudioComponentInitializationScriptRunContext']] = None,
                 script: Optional[pulumi.Input[str]] = None):
        """
        <p>Initialization scripts for studio components.</p>
        :param pulumi.Input[str] launch_profile_protocol_version: <p>The version number of the protocol that is used by the launch profile. The only valid version is "2021-03-31".</p>
        :param pulumi.Input[str] script: <p>The initialization script.</p>
        """
        if launch_profile_protocol_version is not None:
            pulumi.set(__self__, "launch_profile_protocol_version", launch_profile_protocol_version)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if run_context is not None:
            pulumi.set(__self__, "run_context", run_context)
        if script is not None:
            pulumi.set(__self__, "script", script)

    @property
    @pulumi.getter(name="launchProfileProtocolVersion")
    def launch_profile_protocol_version(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The version number of the protocol that is used by the launch profile. The only valid version is "2021-03-31".</p>
        """
        return pulumi.get(self, "launch_profile_protocol_version")

    @launch_profile_protocol_version.setter
    def launch_profile_protocol_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "launch_profile_protocol_version", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input['StudioComponentLaunchProfilePlatform']]:
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input['StudioComponentLaunchProfilePlatform']]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter(name="runContext")
    def run_context(self) -> Optional[pulumi.Input['StudioComponentInitializationScriptRunContext']]:
        return pulumi.get(self, "run_context")

    @run_context.setter
    def run_context(self, value: Optional[pulumi.Input['StudioComponentInitializationScriptRunContext']]):
        pulumi.set(self, "run_context", value)

    @property
    @pulumi.getter
    def script(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The initialization script.</p>
        """
        return pulumi.get(self, "script")

    @script.setter
    def script(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "script", value)


@pulumi.input_type
class StudioComponentLicenseServiceConfigurationArgs:
    def __init__(__self__, *,
                 endpoint: Optional[pulumi.Input[str]] = None):
        """
        <p>The configuration for a license service that is associated with a studio resource.</p>
        :param pulumi.Input[str] endpoint: <p>The endpoint of the license service that is accessed by the studio component resource.</p>
        """
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The endpoint of the license service that is accessed by the studio component resource.</p>
        """
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint", value)


@pulumi.input_type
class StudioComponentScriptParameterKeyValueArgs:
    def __init__(__self__, *,
                 key: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        <p>A parameter for a studio component script, in the form of a key:value pair.</p>
        :param pulumi.Input[str] key: <p>A script parameter key.</p>
        :param pulumi.Input[str] value: <p>A script parameter value.</p>
        """
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        <p>A script parameter key.</p>
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        <p>A script parameter value.</p>
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class StudioComponentSharedFileSystemConfigurationArgs:
    def __init__(__self__, *,
                 endpoint: Optional[pulumi.Input[str]] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 linux_mount_point: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 windows_mount_drive: Optional[pulumi.Input[str]] = None):
        """
        <p>The configuration for a shared file storage system that is associated with a studio resource.</p>
        :param pulumi.Input[str] endpoint: <p>The endpoint of the shared file system that is accessed by the studio component resource.</p>
        :param pulumi.Input[str] file_system_id: <p>The unique identifier for a file system.</p>
        :param pulumi.Input[str] linux_mount_point: <p>The mount location for a shared file system on a Linux virtual workstation.</p>
        :param pulumi.Input[str] share_name: <p>The name of the file share.</p>
        :param pulumi.Input[str] windows_mount_drive: <p>The mount location for a shared file system on a Windows virtual workstation.</p>
        """
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if file_system_id is not None:
            pulumi.set(__self__, "file_system_id", file_system_id)
        if linux_mount_point is not None:
            pulumi.set(__self__, "linux_mount_point", linux_mount_point)
        if share_name is not None:
            pulumi.set(__self__, "share_name", share_name)
        if windows_mount_drive is not None:
            pulumi.set(__self__, "windows_mount_drive", windows_mount_drive)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The endpoint of the shared file system that is accessed by the studio component resource.</p>
        """
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint", value)

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The unique identifier for a file system.</p>
        """
        return pulumi.get(self, "file_system_id")

    @file_system_id.setter
    def file_system_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system_id", value)

    @property
    @pulumi.getter(name="linuxMountPoint")
    def linux_mount_point(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The mount location for a shared file system on a Linux virtual workstation.</p>
        """
        return pulumi.get(self, "linux_mount_point")

    @linux_mount_point.setter
    def linux_mount_point(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "linux_mount_point", value)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The name of the file share.</p>
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_name", value)

    @property
    @pulumi.getter(name="windowsMountDrive")
    def windows_mount_drive(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The mount location for a shared file system on a Windows virtual workstation.</p>
        """
        return pulumi.get(self, "windows_mount_drive")

    @windows_mount_drive.setter
    def windows_mount_drive(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "windows_mount_drive", value)


@pulumi.input_type
class StudioComponentTagsArgs:
    def __init__(__self__):
        pass


@pulumi.input_type
class StudioEncryptionConfigurationArgs:
    def __init__(__self__, *,
                 key_type: pulumi.Input['StudioEncryptionConfigurationKeyType'],
                 key_arn: Optional[pulumi.Input[str]] = None):
        """
        <p>Configuration of the encryption method that is used for the studio.</p>
        :param pulumi.Input[str] key_arn: <p>The ARN for a KMS key that is used to encrypt studio data.</p>
        """
        pulumi.set(__self__, "key_type", key_type)
        if key_arn is not None:
            pulumi.set(__self__, "key_arn", key_arn)

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> pulumi.Input['StudioEncryptionConfigurationKeyType']:
        return pulumi.get(self, "key_type")

    @key_type.setter
    def key_type(self, value: pulumi.Input['StudioEncryptionConfigurationKeyType']):
        pulumi.set(self, "key_type", value)

    @property
    @pulumi.getter(name="keyArn")
    def key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        <p>The ARN for a KMS key that is used to encrypt studio data.</p>
        """
        return pulumi.get(self, "key_arn")

    @key_arn.setter
    def key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_arn", value)


@pulumi.input_type
class StudioTagsArgs:
    def __init__(__self__):
        pass


