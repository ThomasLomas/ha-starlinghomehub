"""Integrations for the Starling Home Hub sensor."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, CONCENTRATION_PARTS_PER_MILLION, LIGHT_LUX, PERCENTAGE, Platform,
                                 UnitOfTemperature)
from homeassistant.helpers.entity import EntityCategory

from custom_components.starling_home_hub.entities.binary_sensor import StarlingHomeHubBinarySensorEntityDescription
from custom_components.starling_home_hub.entities.sensor import StarlingHomeHubSensorEntityDescription

SENSOR_PLATFORMS = {
    Platform.SENSOR: [
        StarlingHomeHubSensorEntityDescription(
            key="current_temperature",
            name="Current Temperature",
            relevant_fn=lambda device: "currentTemperature" in device,
            value_fn=lambda device: device["currentTemperature"],
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="carbon_dioxide_level",
            name="Carbon Dioxide Level",
            relevant_fn=lambda device: "carbonDioxideLevel" in device,
            value_fn=lambda device: device["carbonDioxideLevel"],
            native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="humidity_percent",
            name="Humidity Percentage",
            relevant_fn=lambda device: "humidityPercent" in device,
            value_fn=lambda device: device["humidityPercent"],
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="light_level",
            name="Light Level",
            relevant_fn=lambda device: "lightLevel" in device,
            value_fn=lambda device: device["lightLevel"],
            native_unit_of_measurement=LIGHT_LUX,
            device_class=SensorDeviceClass.ILLUMINANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="pm10_density",
            name="PM10 Density",
            relevant_fn=lambda device: "pm10Density" in device,
            value_fn=lambda device: device["pm10Density"],
            native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
            device_class=SensorDeviceClass.PM10,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="pm25_density",
            name="PM25 Density",
            relevant_fn=lambda device: "pm25Density" in device,
            value_fn=lambda device: device["pm25Density"],
            native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="voc_density",
            name="VOC Density",
            relevant_fn=lambda device: "vocDensity" in device,
            value_fn=lambda device: device["vocDensity"],
            native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
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
        ),
    ],
    Platform.BINARY_SENSOR: [
        StarlingHomeHubBinarySensorEntityDescription(
            key="contact_state",
            name="Contact Sensor",
            relevant_fn=lambda device: "contactState" in device,
            value_fn=lambda device: device["contactState"] == "open",
            device_class=BinarySensorDeviceClass.OPENING
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="leak_detected",
            name="Leak Detected",
            relevant_fn=lambda device: "leakDetected" in device,
            value_fn=lambda device: device["leakDetected"],
            device_class=BinarySensorDeviceClass.MOISTURE
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="motion_detected",
            name="Motion Detected",
            relevant_fn=lambda device: "motionDetected" in device,
            value_fn=lambda device: device["motionDetected"],
            device_class=BinarySensorDeviceClass.MOTION
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="occupancy_detected",
            name="Occupancy Detected",
            relevant_fn=lambda device: "occupancyDetected" in device,
            value_fn=lambda device: device["occupancyDetected"],
            device_class=BinarySensorDeviceClass.OCCUPANCY
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
            key="battery_status",
            name="Battery Status",
            value_fn=lambda device: device["batteryStatus"] != "normal",
            relevant_fn=lambda device: "batteryStatus" in device,
            device_class=BinarySensorDeviceClass.BATTERY,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ],
}
