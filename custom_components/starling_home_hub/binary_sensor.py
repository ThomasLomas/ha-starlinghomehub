"""Sensor platform for starling_home_hub."""
from __future__ import annotations
from collections.abc import Callable

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription, BinarySensorDeviceClass
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
class StarlingHomeHubSmokeDetectorBinarySensorDescription(BinarySensorEntityDescription):
    """Class to describe a Smoke Detector binary sensor."""

    value_fn: Callable[[SmokeDetectorDevice], StateType] | None = None
    relevant_fn: Callable[[SmokeDetectorDevice], StateType] | None = None


BINARY_SENSOR_DESCRIPTIONS: list[BinarySensorEntityDescription] = [
    StarlingHomeHubSmokeDetectorBinarySensorDescription(
        key="smoke_detected",
        name="Smoke Detected",
        relevant_fn=lambda device: "smokeDetected" in device,
        value_fn=lambda device: device["smokeDetected"],
        device_class=BinarySensorDeviceClass.SMOKE
    ),
    StarlingHomeHubSmokeDetectorBinarySensorDescription(
        key="co_detected",
        name="Carbon Monoxide Detected",
        relevant_fn=lambda device: "coDetected" in device,
        value_fn=lambda device: device["coDetected"],
        device_class=BinarySensorDeviceClass.CO
    ),
    StarlingHomeHubSmokeDetectorBinarySensorDescription(
        key="occupancy_detected",
        name="Occupancy Detected",
        relevant_fn=lambda device: "occupancyDetected" in device,
        value_fn=lambda device: device["occupancyDetected"],
        device_class=BinarySensorDeviceClass.OCCUPANCY
    ),
    StarlingHomeHubSmokeDetectorBinarySensorDescription(
        key="battery_status",
        name="Battery Status",
        value_fn=lambda device: device["batteryStatus"] != "normal",
        relevant_fn=lambda device: "batteryStatus" in device,
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubSmokeDetectorBinarySensor] = []
    data: CoordinatorData = coordinator.data

    for device in filter(lambda device: device[1].properties["type"] == "smoke_detector", data.devices.items()):
        for entity_description in BINARY_SENSOR_DESCRIPTIONS:
            if entity_description.relevant_fn and not entity_description.relevant_fn(device[1].properties):
                continue

            entities.append(
                StarlingHomeHubSmokeDetectorBinarySensor(
                    device_id=device[0],
                    coordinator=coordinator,
                    entity_description=entity_description
                )
            )

    async_add_entities(entities, True)


class StarlingHomeHubSmokeDetectorBinarySensor(StarlingHomeHubEntity, BinarySensorEntity):
    """Starling Home Hub Smoke Detector Binary Sensor class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the Smoke Detector Binary Sensor class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        super().__init__(coordinator)

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)
