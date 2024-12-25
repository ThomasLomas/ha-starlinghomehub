"""This module implements the Starling Home Hub Thermostat entity."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, Platform, UnitOfTemperature

from custom_components.starling_home_hub.entities.select import StarlingHomeHubSelectEntityDescription
from custom_components.starling_home_hub.entities.sensor import StarlingHomeHubSensorEntityDescription
from custom_components.starling_home_hub.integrations.base import from_base_entities

THERMOSTAT_PLATFORMS = from_base_entities({
    Platform.SENSOR: [
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
            key="backplate_temperature",
            name="Blackplate Temperature",
            relevant_fn=lambda device: "backplateTemperature" in device,
            value_fn=lambda device: device["backplateTemperature"],
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ],
    Platform.SELECT: [
        StarlingHomeHubSelectEntityDescription(
            key="display_temperature_units",
            name="Display Temperature Units",
            relevant_fn=lambda device: "displayTemperatureUnits" in device,
            value_fn=lambda device: device["displayTemperatureUnits"],
            icon_fn=lambda device: "mdi:temperature-celsius" if device[
                "displayTemperatureUnits"] == "C" else "mdi:temperature-fahrenheit",
            options=["C", "F"],
            update_field="displayTemperatureUnits",
        )
    ],
})
