"""Integrations for the Smoke Detector. This is based on the Sensor integration."""

from copy import deepcopy

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION, Platform

from custom_components.starling_home_hub.entities.binary_sensor import StarlingHomeHubBinarySensorEntityDescription
from custom_components.starling_home_hub.entities.sensor import StarlingHomeHubSensorEntityDescription
from custom_components.starling_home_hub.integrations.sensor import SENSOR_PLATFORMS

SMOKE_CO_DETECTOR_PLATFORMS = deepcopy(SENSOR_PLATFORMS)
SMOKE_CO_DETECTOR_PLATFORMS[Platform.BINARY_SENSOR].extend([
    StarlingHomeHubBinarySensorEntityDescription(
        key="alarm_silenced",
        name="Alarm Silenced",
        relevant_fn=lambda device: "alarmSilenced" in device,
        value_fn=lambda device: device["alarmSilenced"],
        device_class=BinarySensorDeviceClass.SAFETY,
    ),
    StarlingHomeHubBinarySensorEntityDescription(
        key="co_detected",
        name="Carbon Monoxide Detected",
        relevant_fn=lambda device: "coDetected" in device,
        value_fn=lambda device: device["coDetected"],
        device_class=BinarySensorDeviceClass.CO
    ),
    StarlingHomeHubBinarySensorEntityDescription(
        key="smoke_detected",
        name="Smoke Detected",
        relevant_fn=lambda device: "smokeDetected" in device,
        value_fn=lambda device: device["smokeDetected"],
        device_class=BinarySensorDeviceClass.SMOKE
    ),
]),
SMOKE_CO_DETECTOR_PLATFORMS[Platform.SENSOR].extend([
    StarlingHomeHubSensorEntityDescription(
        key="co_detected_level",
        name="Carbon Monoxide Concentration",
        relevant_fn=lambda device: "coLevel" in device,
        value_fn=lambda device: device["coLevel"],
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        device_class=SensorDeviceClass.CO,
        state_class=SensorStateClass.MEASUREMENT,
    ),
])
