"""Starling Home Hub Camera class."""

from __future__ import annotations

import functools
from pathlib import Path

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.components.stream import CONF_EXTRA_PART_WAIT_TIME

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import StarlingHomeHubEntity


PLACEHOLDER = Path(__file__).parent.parent / "camera_placeholder.png"


class StarlingHomeHubBaseCamera(StarlingHomeHubEntity, Camera):
    """Base class for Starling Home Hub camera entities."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        identifier: str = "camera",
    ) -> None:
        """Initialize the Camera class."""
        self.device_id = device_id
        self.coordinator = coordinator
        self._attr_unique_id = f"{device_id}-{identifier}"
        self._attr_supported_features = CameraEntityFeature.STREAM
        self._attr_is_streaming = True
        self._attr_has_entity_name = True

        super().__init__(coordinator)
        Camera.__init__(self)

        device = self.get_device()
        self._attr_name = device.properties["name"]
        self.stream_options[CONF_EXTRA_PART_WAIT_TIME] = 3

    @classmethod
    @functools.cache
    def placeholder_image(cls) -> bytes:
        """Return placeholder image to use when no stream is available."""
        return PLACEHOLDER.read_bytes()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        device = self.get_device()
        return device is not None and device.properties.get("cameraEnabled", False) and device.properties.get("isOnline", False)

    @property
    def is_on(self) -> bool:
        """Return True if the camera is on."""
        return self.get_device() is not None and self.get_device().properties.get("cameraEnabled", False)

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""

        try:
            return await self.coordinator.get_snapshot(self.device_id)
        except Exception as e:
            LOGGER.error(f"Error fetching camera image for {
                         self.device_id}: {e}")
            return await self.hass.async_add_executor_job(self.placeholder_image)

    @property
    def use_stream_for_stills(self) -> bool:
        """Always use the snapshot API for this."""
        return False
