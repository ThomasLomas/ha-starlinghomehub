"""Starling Home Hub Select Entity class."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.helpers.typing import StateType

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


@dataclass
class StarlingHomeHubSelectEntityDescription(SelectEntityDescription):
    """Class to describe a home hub select."""

    value_fn: Callable[[DeviceType], StateType] | None = None
    relevant_fn: Callable[[DeviceType], StateType] | None = None
    update_field: str | None = None
    icon_fn: Callable[[DeviceType], str] | None = None
    options_fn: Callable[[DeviceType], list[str]] | None = None
    prepend_none_option: bool = False


class StarlingHomeHubSelectEntity(StarlingHomeHubEntity, SelectEntity):
    """Starling Home Hub Select Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: StarlingHomeHubSelectEntityDescription,
    ) -> None:
        """Initialize the Select class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"
        self._attr_has_entity_name = True

        if self.entity_description.options is not None:
            self._attr_options = self.entity_description.options
        elif self.entity_description.options_fn is not None:
            self._attr_options = self.entity_description.options_fn(
                self.get_device().properties)

            if self.entity_description.prepend_none_option:
                self._attr_options.insert(0, "None")

        super().__init__(coordinator)

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        return self.entity_description.value_fn(self.get_device().properties)

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        if self.entity_description.icon_fn:
            return self.entity_description.icon_fn(self.get_device().properties)
        return super().icon

    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        if self.entity_description.prepend_none_option and option == "None":
            option = ""
        await self.coordinator.update_device(self.device_id, {
            self.entity_description.update_field: option
        })
