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
    'ChannelTag',
    'PlaybackKeyPairTag',
    'RecordingConfigurationDestinationConfiguration',
    'RecordingConfigurationS3DestinationConfiguration',
    'RecordingConfigurationTag',
    'RecordingConfigurationThumbnailConfiguration',
    'StreamKeyTag',
]

@pulumi.output_type
class ChannelTag(dict):
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
class PlaybackKeyPairTag(dict):
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
class RecordingConfigurationDestinationConfiguration(dict):
    """
    Recording Destination Configuration.
    """
    def __init__(__self__, *,
                 s3: 'outputs.RecordingConfigurationS3DestinationConfiguration'):
        """
        Recording Destination Configuration.
        """
        pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter
    def s3(self) -> 'outputs.RecordingConfigurationS3DestinationConfiguration':
        return pulumi.get(self, "s3")


@pulumi.output_type
class RecordingConfigurationS3DestinationConfiguration(dict):
    """
    Recording S3 Destination Configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RecordingConfigurationS3DestinationConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RecordingConfigurationS3DestinationConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RecordingConfigurationS3DestinationConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: str):
        """
        Recording S3 Destination Configuration.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        return pulumi.get(self, "bucket_name")


@pulumi.output_type
class RecordingConfigurationTag(dict):
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
class RecordingConfigurationThumbnailConfiguration(dict):
    """
    Recording Thumbnail Configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "recordingMode":
            suggest = "recording_mode"
        elif key == "targetIntervalSeconds":
            suggest = "target_interval_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RecordingConfigurationThumbnailConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RecordingConfigurationThumbnailConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RecordingConfigurationThumbnailConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 recording_mode: 'RecordingConfigurationThumbnailConfigurationRecordingMode',
                 target_interval_seconds: Optional[int] = None):
        """
        Recording Thumbnail Configuration.
        :param 'RecordingConfigurationThumbnailConfigurationRecordingMode' recording_mode: Thumbnail Recording Mode, which determines whether thumbnails are recorded at an interval or are disabled.
        :param int target_interval_seconds: Thumbnail recording Target Interval Seconds defines the interval at which thumbnails are recorded. This field is required if RecordingMode is INTERVAL.
        """
        pulumi.set(__self__, "recording_mode", recording_mode)
        if target_interval_seconds is not None:
            pulumi.set(__self__, "target_interval_seconds", target_interval_seconds)

    @property
    @pulumi.getter(name="recordingMode")
    def recording_mode(self) -> 'RecordingConfigurationThumbnailConfigurationRecordingMode':
        """
        Thumbnail Recording Mode, which determines whether thumbnails are recorded at an interval or are disabled.
        """
        return pulumi.get(self, "recording_mode")

    @property
    @pulumi.getter(name="targetIntervalSeconds")
    def target_interval_seconds(self) -> Optional[int]:
        """
        Thumbnail recording Target Interval Seconds defines the interval at which thumbnails are recorded. This field is required if RecordingMode is INTERVAL.
        """
        return pulumi.get(self, "target_interval_seconds")


@pulumi.output_type
class StreamKeyTag(dict):
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


