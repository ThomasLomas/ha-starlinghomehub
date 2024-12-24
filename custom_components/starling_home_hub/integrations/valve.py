"""Integration for switches."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.valve import ValveDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import Platform, PERCENTAGE
from homeassistant.helpers.entity import EntityCategory

from custom_components.starling_home_hub.entities.binary_sensor import StarlingHomeHubBinarySensorEntityDescription
from custom_components.starling_home_hub.entities.sensor import StarlingHomeHubSensorEntityDescription
from custom_components.starling_home_hub.entities.valve import StarlingHomeHubValveEntityDescription

VALVE_PLATFORMS = {
    Platform.VALVE: [
        StarlingHomeHubValveEntityDescription(
            key="is_on",
            name="Is On",
            relevant_fn=lambda device: "isOn" in device,
            value_fn=lambda device: device["isOn"],
            update_field="isOn",
            device_class=ValveDeviceClass.WATER,
        ),
    ],
    Platform.BINARY_SENSOR: [
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
            key="battery_status",
            name="Battery Status",
            value_fn=lambda device: device["batteryStatus"] != "normal",
            relevant_fn=lambda device: "batteryStatus" in device,
            device_class=BinarySensorDeviceClass.BATTERY,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ],
    Platform.SENSOR: [
        StarlingHomeHubSensorEntityDescription(
            key="battery_level",
            name="Battery Level",
            relevant_fn=lambda device: "batteryLevel" in device,
            value_fn=lambda device: device["batteryLevel"],
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.BATTERY,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ]
}
