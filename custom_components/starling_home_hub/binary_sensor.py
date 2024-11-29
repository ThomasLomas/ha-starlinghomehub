"""Sensor platform for starling_home_hub."""
from __future__ import annotations
from collections.abc import Callable

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription, BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.typing import StateType
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, LOGGER
from .coordinator import StarlingHomeHubDataUpdateCoordinator
from .entity import StarlingHomeHubEntity
from .models import CoordinatorData, Device

from dataclasses import dataclass


@dataclass
class StarlingHomeHubNestProtectBinarySensorDescription(BinarySensorEntityDescription):
    """Class to describe an Nest Protect sensor."""

    value_fn: Callable[[Device], StateType] | None = None


BINARY_SENSOR_DESCRIPTIONS: list[BinarySensorEntityDescription] = [
    StarlingHomeHubNestProtectBinarySensorDescription(
        key="smoke_detected",
        name="Smoke Detected",
        value_fn=lambda device: device["smokeDetected"],
        device_class=BinarySensorDeviceClass.SMOKE
    ),
    StarlingHomeHubNestProtectBinarySensorDescription(
        key="co_detected",
        name="Carbon Monoxide Detected",
        value_fn=lambda device: device["coDetected"],
        device_class=BinarySensorDeviceClass.CO
    ),
    StarlingHomeHubNestProtectBinarySensorDescription(
        key="occupancy_detected",
        name="Occupancy Detected",
        value_fn=lambda device: device.get("occupancyDetected", None),
        device_class=BinarySensorDeviceClass.OCCUPANCY
    ),
    StarlingHomeHubNestProtectBinarySensorDescription(
        key="battery_status",
        name="Battery Status",
        value_fn=lambda device: device["batteryStatus"] != "normal",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubNestProtectSensor] = []
    data: CoordinatorData = coordinator.data

    LOGGER.debug(data.devices)

    for device in filter(lambda device: device[1].properties["type"] == "protect", data.devices.items()):
        for entity_description in BINARY_SENSOR_DESCRIPTIONS:
            entities.append(
                StarlingHomeHubNestProtectSensor(
                    device_id=device[0],
                    coordinator=coordinator,
                    entity_description=entity_description
                )
            )

    async_add_entities(entities, True)


class StarlingHomeHubNestProtectSensor(StarlingHomeHubEntity, BinarySensorEntity):
    """Starling Home Hub Nest Protect Sensor class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the Nest Protect Sensor class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        super().__init__(coordinator)

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)
