"""Sensor platform for starling_home_hub."""
from __future__ import annotations
from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass
from homeassistant.helpers.typing import StateType
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import StarlingHomeHubDataUpdateCoordinator
from .entity import StarlingHomeHubEntity
from .models import CoordinatorData, Device

from dataclasses import dataclass


@dataclass
class StarlingHomeHubNestProtectSensorDescription(SensorEntityDescription):
    """Class to describe an Nest Protect sensor."""

    value_fn: Callable[[Device], StateType] | None = None


SENSOR_DESCRIPTIONS: list[SensorEntityDescription] = [
    StarlingHomeHubNestProtectSensorDescription(
        key="smoke_detected_detail",
        name="Smoke Detected Detail",
        value_fn=lambda device: device["smokeStateDetail"] if "smokeStateDetail" in device else None,
        device_class=SensorDeviceClass.ENUM,
        options=["ok", "warn", "emergency"]
    ),
    StarlingHomeHubNestProtectSensorDescription(
        key="co_detected_detail",
        name="Carbon Monoxide Detected Detail",
        value_fn=lambda device: device["coStateDetail"] if "coStateDetail" in device else None,
        device_class=SensorDeviceClass.ENUM,
        options=["ok", "warn", "emergency"]
    )
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubNestProtectSensor] = []
    data: CoordinatorData = coordinator.data

    for device in filter(lambda device: device[1].properties["type"] == "protect", data.devices.items()):
        for entity_description in SENSOR_DESCRIPTIONS:
            entities.append(
                StarlingHomeHubNestProtectSensor(
                    device_id=device[0],
                    coordinator=coordinator,
                    entity_description=entity_description
                )
            )

    async_add_entities(entities, True)


class StarlingHomeHubNestProtectSensor(StarlingHomeHubEntity, SensorEntity):
    """Starling Home Hub Nest Protect Sensor class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the Nest Protect Sensor class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        super().__init__(coordinator)

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)
