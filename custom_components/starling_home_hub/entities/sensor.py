"""Starling Home Hub Sensor Entity class."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass
class StarlingHomeHubSensorEntityDescription(SensorEntityDescription):
    """Class to describe a home hub sensor."""

    value_fn: Callable[[DeviceType], StateType] | None = None
    relevant_fn: Callable[[DeviceType], StateType] | None = None


class StarlingHomeHubSensorEntity(StarlingHomeHubEntity, SensorEntity):
    """Starling Home Hub Sensor Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubSensorEntityDescription,
    ) -> None:
        """Initialize the Sensor Entity class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True

        super().__init__(coordinator)

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)
