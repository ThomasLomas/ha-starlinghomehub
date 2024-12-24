"""Starling Home Hub Lock Entity class."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass
class StarlingHomeHubLockEntityDescription(LockEntityDescription):
    """Class to describe a home hub Lock."""

    current_state_field: str = "currentState"
    target_state_field: str = "targetState"
    relevant_fn: Callable[[DeviceType], StateType] | None = None
    # icon_fn: Callable[[DeviceType], str] | None = None


class StarlingHomeHubLockEntity(StarlingHomeHubEntity, LockEntity):
    """Starling Home Hub Lock Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubLockEntityDescription,
    ) -> None:
        """Initialize the Lock class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True

        super().__init__(coordinator)
