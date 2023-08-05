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
    'ExperimentMetricGoalObject',
    'ExperimentOnlineAbConfigObject',
    'ExperimentRunningStatusObject',
    'ExperimentTag',
    'ExperimentTreatmentObject',
    'ExperimentTreatmentToWeight',
    'FeatureEntityOverride',
    'FeatureTag',
    'FeatureVariationObject',
    'LaunchExecutionStatusObject',
    'LaunchGroupObject',
    'LaunchGroupToWeight',
    'LaunchMetricDefinitionObject',
    'LaunchStepConfig',
    'LaunchTag',
    'ProjectDataDeliveryObject',
    'ProjectS3Destination',
    'ProjectTag',
]

@pulumi.output_type
class ExperimentMetricGoalObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "desiredChange":
            suggest = "desired_change"
        elif key == "entityIdKey":
            suggest = "entity_id_key"
        elif key == "eventPattern":
            suggest = "event_pattern"
        elif key == "metricName":
            suggest = "metric_name"
        elif key == "valueKey":
            suggest = "value_key"
        elif key == "unitLabel":
            suggest = "unit_label"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentMetricGoalObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentMetricGoalObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentMetricGoalObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 desired_change: 'ExperimentMetricGoalObjectDesiredChange',
                 entity_id_key: str,
                 event_pattern: str,
                 metric_name: str,
                 value_key: str,
                 unit_label: Optional[str] = None):
        """
        :param str entity_id_key: The JSON path to reference the entity id in the event.
        :param str event_pattern: Event patterns have the same structure as the events they match. Rules use event patterns to select events. An event pattern either matches an event or it doesn't.
        :param str value_key: The JSON path to reference the numerical metric value in the event.
        """
        pulumi.set(__self__, "desired_change", desired_change)
        pulumi.set(__self__, "entity_id_key", entity_id_key)
        pulumi.set(__self__, "event_pattern", event_pattern)
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "value_key", value_key)
        if unit_label is not None:
            pulumi.set(__self__, "unit_label", unit_label)

    @property
    @pulumi.getter(name="desiredChange")
    def desired_change(self) -> 'ExperimentMetricGoalObjectDesiredChange':
        return pulumi.get(self, "desired_change")

    @property
    @pulumi.getter(name="entityIdKey")
    def entity_id_key(self) -> str:
        """
        The JSON path to reference the entity id in the event.
        """
        return pulumi.get(self, "entity_id_key")

    @property
    @pulumi.getter(name="eventPattern")
    def event_pattern(self) -> str:
        """
        Event patterns have the same structure as the events they match. Rules use event patterns to select events. An event pattern either matches an event or it doesn't.
        """
        return pulumi.get(self, "event_pattern")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter(name="valueKey")
    def value_key(self) -> str:
        """
        The JSON path to reference the numerical metric value in the event.
        """
        return pulumi.get(self, "value_key")

    @property
    @pulumi.getter(name="unitLabel")
    def unit_label(self) -> Optional[str]:
        return pulumi.get(self, "unit_label")


@pulumi.output_type
class ExperimentOnlineAbConfigObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "controlTreatmentName":
            suggest = "control_treatment_name"
        elif key == "treatmentWeights":
            suggest = "treatment_weights"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentOnlineAbConfigObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentOnlineAbConfigObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentOnlineAbConfigObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 control_treatment_name: Optional[str] = None,
                 treatment_weights: Optional[Sequence['outputs.ExperimentTreatmentToWeight']] = None):
        if control_treatment_name is not None:
            pulumi.set(__self__, "control_treatment_name", control_treatment_name)
        if treatment_weights is not None:
            pulumi.set(__self__, "treatment_weights", treatment_weights)

    @property
    @pulumi.getter(name="controlTreatmentName")
    def control_treatment_name(self) -> Optional[str]:
        return pulumi.get(self, "control_treatment_name")

    @property
    @pulumi.getter(name="treatmentWeights")
    def treatment_weights(self) -> Optional[Sequence['outputs.ExperimentTreatmentToWeight']]:
        return pulumi.get(self, "treatment_weights")


@pulumi.output_type
class ExperimentRunningStatusObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "analysisCompleteTime":
            suggest = "analysis_complete_time"
        elif key == "desiredState":
            suggest = "desired_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentRunningStatusObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentRunningStatusObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentRunningStatusObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 analysis_complete_time: Optional[str] = None,
                 desired_state: Optional[str] = None,
                 reason: Optional[str] = None,
                 status: Optional[str] = None):
        """
        :param str analysis_complete_time: Provide the analysis Completion time for an experiment
        :param str desired_state: Provide CANCELLED or COMPLETED desired state when stopping an experiment
        :param str reason: Reason is a required input for stopping the experiment
        :param str status: Provide START or STOP action to apply on an experiment
        """
        if analysis_complete_time is not None:
            pulumi.set(__self__, "analysis_complete_time", analysis_complete_time)
        if desired_state is not None:
            pulumi.set(__self__, "desired_state", desired_state)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="analysisCompleteTime")
    def analysis_complete_time(self) -> Optional[str]:
        """
        Provide the analysis Completion time for an experiment
        """
        return pulumi.get(self, "analysis_complete_time")

    @property
    @pulumi.getter(name="desiredState")
    def desired_state(self) -> Optional[str]:
        """
        Provide CANCELLED or COMPLETED desired state when stopping an experiment
        """
        return pulumi.get(self, "desired_state")

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        """
        Reason is a required input for stopping the experiment
        """
        return pulumi.get(self, "reason")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Provide START or STOP action to apply on an experiment
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class ExperimentTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ExperimentTreatmentObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "treatmentName":
            suggest = "treatment_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTreatmentObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTreatmentObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTreatmentObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 feature: str,
                 treatment_name: str,
                 variation: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "feature", feature)
        pulumi.set(__self__, "treatment_name", treatment_name)
        pulumi.set(__self__, "variation", variation)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def feature(self) -> str:
        return pulumi.get(self, "feature")

    @property
    @pulumi.getter(name="treatmentName")
    def treatment_name(self) -> str:
        return pulumi.get(self, "treatment_name")

    @property
    @pulumi.getter
    def variation(self) -> str:
        return pulumi.get(self, "variation")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class ExperimentTreatmentToWeight(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "splitWeight":
            suggest = "split_weight"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTreatmentToWeight. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTreatmentToWeight.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTreatmentToWeight.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 split_weight: int,
                 treatment: str):
        pulumi.set(__self__, "split_weight", split_weight)
        pulumi.set(__self__, "treatment", treatment)

    @property
    @pulumi.getter(name="splitWeight")
    def split_weight(self) -> int:
        return pulumi.get(self, "split_weight")

    @property
    @pulumi.getter
    def treatment(self) -> str:
        return pulumi.get(self, "treatment")


@pulumi.output_type
class FeatureEntityOverride(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "entityId":
            suggest = "entity_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FeatureEntityOverride. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FeatureEntityOverride.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FeatureEntityOverride.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 entity_id: Optional[str] = None,
                 variation: Optional[str] = None):
        if entity_id is not None:
            pulumi.set(__self__, "entity_id", entity_id)
        if variation is not None:
            pulumi.set(__self__, "variation", variation)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> Optional[str]:
        return pulumi.get(self, "entity_id")

    @property
    @pulumi.getter
    def variation(self) -> Optional[str]:
        return pulumi.get(self, "variation")


@pulumi.output_type
class FeatureTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class FeatureVariationObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "booleanValue":
            suggest = "boolean_value"
        elif key == "doubleValue":
            suggest = "double_value"
        elif key == "longValue":
            suggest = "long_value"
        elif key == "stringValue":
            suggest = "string_value"
        elif key == "variationName":
            suggest = "variation_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FeatureVariationObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FeatureVariationObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FeatureVariationObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 boolean_value: Optional[bool] = None,
                 double_value: Optional[float] = None,
                 long_value: Optional[float] = None,
                 string_value: Optional[str] = None,
                 variation_name: Optional[str] = None):
        if boolean_value is not None:
            pulumi.set(__self__, "boolean_value", boolean_value)
        if double_value is not None:
            pulumi.set(__self__, "double_value", double_value)
        if long_value is not None:
            pulumi.set(__self__, "long_value", long_value)
        if string_value is not None:
            pulumi.set(__self__, "string_value", string_value)
        if variation_name is not None:
            pulumi.set(__self__, "variation_name", variation_name)

    @property
    @pulumi.getter(name="booleanValue")
    def boolean_value(self) -> Optional[bool]:
        return pulumi.get(self, "boolean_value")

    @property
    @pulumi.getter(name="doubleValue")
    def double_value(self) -> Optional[float]:
        return pulumi.get(self, "double_value")

    @property
    @pulumi.getter(name="longValue")
    def long_value(self) -> Optional[float]:
        return pulumi.get(self, "long_value")

    @property
    @pulumi.getter(name="stringValue")
    def string_value(self) -> Optional[str]:
        return pulumi.get(self, "string_value")

    @property
    @pulumi.getter(name="variationName")
    def variation_name(self) -> Optional[str]:
        return pulumi.get(self, "variation_name")


@pulumi.output_type
class LaunchExecutionStatusObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "desiredState":
            suggest = "desired_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchExecutionStatusObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchExecutionStatusObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchExecutionStatusObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 status: str,
                 desired_state: Optional[str] = None,
                 reason: Optional[str] = None):
        """
        :param str status: Provide START or STOP action to apply on a launch
        :param str desired_state: Provide CANCELLED or COMPLETED as the launch desired state. Defaults to Completed if not provided.
        :param str reason: Provide a reason for stopping the launch. Defaults to empty if not provided.
        """
        pulumi.set(__self__, "status", status)
        if desired_state is not None:
            pulumi.set(__self__, "desired_state", desired_state)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Provide START or STOP action to apply on a launch
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="desiredState")
    def desired_state(self) -> Optional[str]:
        """
        Provide CANCELLED or COMPLETED as the launch desired state. Defaults to Completed if not provided.
        """
        return pulumi.get(self, "desired_state")

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        """
        Provide a reason for stopping the launch. Defaults to empty if not provided.
        """
        return pulumi.get(self, "reason")


@pulumi.output_type
class LaunchGroupObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupName":
            suggest = "group_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchGroupObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchGroupObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchGroupObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 feature: str,
                 group_name: str,
                 variation: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "feature", feature)
        pulumi.set(__self__, "group_name", group_name)
        pulumi.set(__self__, "variation", variation)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def feature(self) -> str:
        return pulumi.get(self, "feature")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> str:
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter
    def variation(self) -> str:
        return pulumi.get(self, "variation")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class LaunchGroupToWeight(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupName":
            suggest = "group_name"
        elif key == "splitWeight":
            suggest = "split_weight"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchGroupToWeight. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchGroupToWeight.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchGroupToWeight.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 group_name: str,
                 split_weight: int):
        pulumi.set(__self__, "group_name", group_name)
        pulumi.set(__self__, "split_weight", split_weight)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> str:
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter(name="splitWeight")
    def split_weight(self) -> int:
        return pulumi.get(self, "split_weight")


@pulumi.output_type
class LaunchMetricDefinitionObject(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "entityIdKey":
            suggest = "entity_id_key"
        elif key == "eventPattern":
            suggest = "event_pattern"
        elif key == "metricName":
            suggest = "metric_name"
        elif key == "valueKey":
            suggest = "value_key"
        elif key == "unitLabel":
            suggest = "unit_label"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchMetricDefinitionObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchMetricDefinitionObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchMetricDefinitionObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 entity_id_key: str,
                 event_pattern: str,
                 metric_name: str,
                 value_key: str,
                 unit_label: Optional[str] = None):
        """
        :param str entity_id_key: The JSON path to reference the entity id in the event.
        :param str event_pattern: Event patterns have the same structure as the events they match. Rules use event patterns to select events. An event pattern either matches an event or it doesn't.
        :param str value_key: The JSON path to reference the numerical metric value in the event.
        """
        pulumi.set(__self__, "entity_id_key", entity_id_key)
        pulumi.set(__self__, "event_pattern", event_pattern)
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "value_key", value_key)
        if unit_label is not None:
            pulumi.set(__self__, "unit_label", unit_label)

    @property
    @pulumi.getter(name="entityIdKey")
    def entity_id_key(self) -> str:
        """
        The JSON path to reference the entity id in the event.
        """
        return pulumi.get(self, "entity_id_key")

    @property
    @pulumi.getter(name="eventPattern")
    def event_pattern(self) -> str:
        """
        Event patterns have the same structure as the events they match. Rules use event patterns to select events. An event pattern either matches an event or it doesn't.
        """
        return pulumi.get(self, "event_pattern")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter(name="valueKey")
    def value_key(self) -> str:
        """
        The JSON path to reference the numerical metric value in the event.
        """
        return pulumi.get(self, "value_key")

    @property
    @pulumi.getter(name="unitLabel")
    def unit_label(self) -> Optional[str]:
        return pulumi.get(self, "unit_label")


@pulumi.output_type
class LaunchStepConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupWeights":
            suggest = "group_weights"
        elif key == "startTime":
            suggest = "start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchStepConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchStepConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchStepConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 group_weights: Sequence['outputs.LaunchGroupToWeight'],
                 start_time: str):
        pulumi.set(__self__, "group_weights", group_weights)
        pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="groupWeights")
    def group_weights(self) -> Sequence['outputs.LaunchGroupToWeight']:
        return pulumi.get(self, "group_weights")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        return pulumi.get(self, "start_time")


@pulumi.output_type
class LaunchTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ProjectDataDeliveryObject(dict):
    """
    Destinations for data.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ProjectDataDeliveryObject. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ProjectDataDeliveryObject.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ProjectDataDeliveryObject.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group: Optional[str] = None,
                 s3: Optional['outputs.ProjectS3Destination'] = None):
        """
        Destinations for data.
        """
        if log_group is not None:
            pulumi.set(__self__, "log_group", log_group)
        if s3 is not None:
            pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> Optional[str]:
        return pulumi.get(self, "log_group")

    @property
    @pulumi.getter
    def s3(self) -> Optional['outputs.ProjectS3Destination']:
        return pulumi.get(self, "s3")


@pulumi.output_type
class ProjectS3Destination(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ProjectS3Destination. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ProjectS3Destination.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ProjectS3Destination.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: str,
                 prefix: Optional[str] = None):
        pulumi.set(__self__, "bucket_name", bucket_name)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        return pulumi.get(self, "prefix")


@pulumi.output_type
class ProjectTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


