"""Starling Home Hub Lock Entity class."""

from __future__ import annotations

from typing import Optional

from homeassistant.components.fan import FanEntity, FanEntityFeature

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import DeviceType, StarlingHomeHubEntity


class StarlingHomeHubFanEntity(StarlingHomeHubEntity, FanEntity):
    """Starling Home Hub Fan Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
    ) -> None:
        """Initialize the Fan class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self._attr_unique_id = f"{device_id}-fan"
        self._attr_has_entity_name = True

        device = self.get_device()

        self._attr_supported_features = (
            FanEntityFeature.TURN_ON,
            FanEntityFeature.TURN_OFF,
        )

        if "fanSpeed" in device:
            self._attr_supported_features |= FanEntityFeature.SET_SPEED

        super().__init__(coordinator)

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        await self.coordinator.update_device(self.device_id, {
            "fanSpeed": percentage
        })

    async def async_turn_on(self, percentage: Optional[int] = None) -> None:
        """Turn on the fan."""
        payload = {
            "isOn": True
        }

        if percentage is not None:
            payload["fanSpeed"] = percentage

        await self.coordinator.update_device(self.device_id, payload)

    async def async_turn_off(self) -> None:
        """Turn the fan off."""
        await self.coordinator.update_device(self.device_id, {
            "isOn": False
        })
