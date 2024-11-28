"""Integrations for the Smoke Detector."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION, PERCENTAGE, Platform
from homeassistant.helpers.entity import EntityCategory

from custom_components.starling_home_hub.integrations import StarlingHomeHubBinarySensorDescription, StarlingHomeHubSensorDescription

SMOKE_DETECTOR_PLATFORMS = {
    Platform.SENSOR: [
        StarlingHomeHubSensorDescription(
            key="co_detected_level",
            name="Carbon Monoxide Concentration",
            relevant_fn=lambda device: "coLevel" in device,
            value_fn=lambda device: device["coLevel"],
            native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            device_class=SensorDeviceClass.CO,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorDescription(
            key="battery_level",
            name="Battery Level",
            relevant_fn=lambda device: "batteryLevel" in device,
            value_fn=lambda device: device["batteryLevel"],
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.BATTERY,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
        )
    ],
    Platform.BINARY_SENSOR: [
        StarlingHomeHubBinarySensorDescription(
            key="smoke_detected",
            name="Smoke Detected",
            relevant_fn=lambda device: "smokeDetected" in device,
            value_fn=lambda device: device["smokeDetected"],
            device_class=BinarySensorDeviceClass.SMOKE
        ),
        StarlingHomeHubBinarySensorDescription(
            key="co_detected",
            name="Carbon Monoxide Detected",
            relevant_fn=lambda device: "coDetected" in device,
            value_fn=lambda device: device["coDetected"],
            device_class=BinarySensorDeviceClass.CO
        ),
        StarlingHomeHubBinarySensorDescription(
            key="occupancy_detected",
            name="Occupancy Detected",
            relevant_fn=lambda device: "occupancyDetected" in device,
            value_fn=lambda device: device["occupancyDetected"],
            device_class=BinarySensorDeviceClass.OCCUPANCY
        ),
        StarlingHomeHubBinarySensorDescription(
            key="battery_status",
            name="Battery Status",
            value_fn=lambda device: device["batteryStatus"] != "normal",
            relevant_fn=lambda device: "batteryStatus" in device,
            device_class=BinarySensorDeviceClass.BATTERY,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ]
}
