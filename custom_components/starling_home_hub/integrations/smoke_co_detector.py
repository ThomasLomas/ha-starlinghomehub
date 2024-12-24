"""Integrations for the Smoke Detector."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION, PERCENTAGE, Platform
from homeassistant.helpers.entity import EntityCategory

from custom_components.starling_home_hub.entities.binary_sensor import StarlingHomeHubBinarySensorEntityDescription
from custom_components.starling_home_hub.entities.sensor import StarlingHomeHubSensorEntityDescription

SMOKE_CO_DETECTOR_PLATFORMS = {
    Platform.SENSOR: [
        StarlingHomeHubSensorEntityDescription(
            key="co_detected_level",
            name="Carbon Monoxide Concentration",
            relevant_fn=lambda device: "coLevel" in device,
            value_fn=lambda device: device["coLevel"],
            native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            device_class=SensorDeviceClass.CO,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
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
        StarlingHomeHubBinarySensorEntityDescription(
            key="smoke_detected",
            name="Smoke Detected",
            relevant_fn=lambda device: "smokeDetected" in device,
            value_fn=lambda device: device["smokeDetected"],
            device_class=BinarySensorDeviceClass.SMOKE
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="co_detected",
            name="Carbon Monoxide Detected",
            relevant_fn=lambda device: "coDetected" in device,
            value_fn=lambda device: device["coDetected"],
            device_class=BinarySensorDeviceClass.CO
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="occupancy_detected",
            name="Occupancy Detected",
            relevant_fn=lambda device: "occupancyDetected" in device,
            value_fn=lambda device: device["occupancyDetected"],
            device_class=BinarySensorDeviceClass.OCCUPANCY
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="battery_status",
            name="Battery Status",
            value_fn=lambda device: device["batteryStatus"] != "normal",
            relevant_fn=lambda device: "batteryStatus" in device,
            device_class=BinarySensorDeviceClass.BATTERY,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="is_online",
            name="Is Online",
            relevant_fn=lambda device: "isOnline" in device,
            value_fn=lambda device: device["isOnline"],
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="battery_charging",
            name="Battery Charging",
            relevant_fn=lambda device: "batteryIsCharging" in device,
            value_fn=lambda device: device["batteryIsCharging"],
            device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="alarm_silenced",
            name="Alarm Silenced",
            relevant_fn=lambda device: "alarmSilenced" in device,
            value_fn=lambda device: device["alarmSilenced"],
            device_class=BinarySensorDeviceClass.SAFETY,
        ),
    ]
}
