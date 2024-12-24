"""Starling Home Hub Cover Entity class."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.cover import CoverEntity, CoverEntityDescription, CoverEntityFeature
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass
class StarlingHomeHubCoverEntityDescription(CoverEntityDescription):
    """Class to describe a home hub Cover."""

    current_state_field: str = "currentState"
    target_state_field: str = "targetState"
    relevant_fn: Callable[[DeviceType], StateType] | None = None
    # icon_fn: Callable[[DeviceType], str] | None = None


class StarlingHomeHubCoverEntity(StarlingHomeHubEntity, CoverEntity):
    """Starling Home Hub Cover Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubCoverEntityDescription,
    ) -> None:
        """Initialize the Cover class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True
        self.device_class = entity_description.device_class
        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

        super().__init__(coordinator)

    @property
    def is_closed(self) -> bool:
        """Return if device is closed."""
        return self.get_device().properties[self.entity_description.current_state_field] == "closed"

    @property
    def is_opening(self) -> bool:
        """Return if device is opening."""
        return self.get_device().properties[self.entity_description.current_state_field] == "opening"

    @property
    def is_closing(self) -> bool:
        """Return if device is closing."""
        return self.get_device().properties[self.entity_description.current_state_field] == "closing"

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.target_state_field: "open"
        })

    async def async_close_cover(self, **kwargs):
        """Close cover."""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.target_state_field: "closed"
        })
