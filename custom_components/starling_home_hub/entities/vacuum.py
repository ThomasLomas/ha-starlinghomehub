"""Entity for vacuums."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.vacuum import StateVacuumEntity, StateVacuumEntityDescription
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass
class StarlingHomeHubVacuumEntityDescription(StateVacuumEntityDescription):
    """Class to describe a home hub Vacuum."""

    value_fn: Callable[[DeviceType], StateType] | None = None
    relevant_fn: Callable[[DeviceType], StateType] | None = None
    update_field: str | None = None


class StarlingHomeHubVacuumEntity(StarlingHomeHubEntity, StateVacuumEntity):
    """Starling Home Hub Vacuum Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubVacuumEntityDescription,
    ) -> None:
        """Initialize the Vacuum class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True

        super().__init__(coordinator)
