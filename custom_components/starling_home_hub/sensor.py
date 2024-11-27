"""Sensor platform for starling_home_hub."""
from __future__ import annotations
from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.typing import StateType
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from custom_components.starling_home_hub.models.api.device.smoke_detector import SmokeDetectorDevice
from custom_components.starling_home_hub.models.coordinator import CoordinatorData

from .const import DOMAIN
from .coordinator import StarlingHomeHubDataUpdateCoordinator
from .entity import StarlingHomeHubEntity

from dataclasses import dataclass


@dataclass
class StarlingHomeHubSmokeDetectorSensorDescription(SensorEntityDescription):
    """Class to describe a smoke detector sensor."""

    value_fn: Callable[[SmokeDetectorDevice], StateType] | None = None
    relevant_fn: Callable[[SmokeDetectorDevice], StateType] | None = None


SENSOR_DESCRIPTIONS: list[SensorEntityDescription] = [
    StarlingHomeHubSmokeDetectorSensorDescription(
        key="co_detected_level",
        name="Carbon Monoxide Concentration",
        relevant_fn=lambda device: "coLevel" in device,
        value_fn=lambda device: device["coLevel"],
        native_unit_of_measurement="ppm",
        device_class=SensorDeviceClass.CO,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StarlingHomeHubSmokeDetectorSensorDescription(
        key="battery_level",
        name="Battery Level",
        relevant_fn=lambda device: "batteryLevel" in device,
        value_fn=lambda device: device["batteryLevel"],
        native_unit_of_measurement="%",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    )
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubSmokeDetectorSensor] = []
    data: CoordinatorData = coordinator.data

    for device in filter(lambda device: device[1].properties["type"] == "smoke_detector", data.devices.items()):
        for entity_description in SENSOR_DESCRIPTIONS:
            if not entity_description.relevant_fn or entity_description.relevant_fn(device[1].properties):
                entities.append(
                    StarlingHomeHubSmokeDetectorSensor(
                        device_id=device[0],
                        coordinator=coordinator,
                        entity_description=entity_description
                    )
                )

    async_add_entities(entities, True)


class StarlingHomeHubSmokeDetectorSensor(StarlingHomeHubEntity, SensorEntity):
    """Starling Home Hub Smoke Detector Sensor class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the Smoke Detector Sensor class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        super().__init__(coordinator)

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)
