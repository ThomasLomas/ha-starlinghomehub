"""Starling Home Hub Switch Entity class."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass
class StarlingHomeHubSwitchEntityDescription(SwitchEntityDescription):
    """Class to describe a home hub switch."""

    value_fn: Callable[[DeviceType], StateType] | None = None
    relevant_fn: Callable[[DeviceType], StateType] | None = None
    update_field: str | None = None


class StarlingHomeHubSwitchEntity(StarlingHomeHubEntity, SwitchEntity):
    """Starling Home Hub Switch Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubSwitchEntityDescription,
    ) -> None:
        """Initialize the Switch class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True

        super().__init__(coordinator)

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return self.entity_description.value_fn(self.get_device().properties)

    async def async_turn_on(self) -> None:
        """Turn the switch on."""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.update_field: True
        })

    async def async_turn_off(self) -> None:
        """Turn the switch off."""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.update_field: False
        })
