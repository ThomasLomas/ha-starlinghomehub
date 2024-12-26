"""Starling Home Hub Valve Entity class."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.valve import ValveEntity, ValveEntityDescription, ValveEntityFeature
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass(frozen=True)
class StarlingHomeHubValveEntityDescription(ValveEntityDescription):
    """Class to describe a home hub Valve."""

    value_fn: Callable[[DeviceType], StateType] | None = None
    relevant_fn: Callable[[DeviceType], StateType] | None = None
    update_field: str | None = None


class StarlingHomeHubValveEntity(StarlingHomeHubEntity, ValveEntity):
    """Starling Home Hub Valve Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubValveEntityDescription,
    ) -> None:
        """Initialize the Valve class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True
        self._attr_supported_features = ValveEntityFeature.CLOSE | ValveEntityFeature.OPEN
        self._attr_reports_position = False

        super().__init__(coordinator)

    @property
    def is_closed(self) -> bool:
        """Returns if the valve is closed."""
        return not self.entity_description.value_fn(self.get_device().properties)

    async def async_open_valve(self) -> None:
        """Open the valve."""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.update_field: True
        })

    async def async_close_valve(self) -> None:
        """Close the valve."""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.update_field: False
        })
