"""Support for cameras from Starling Home Hub."""

from __future__ import annotations

import asyncio
import base64
import functools
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.camera import Camera, CameraEntityFeature, StreamType
from homeassistant.components.stream import CONF_EXTRA_PART_WAIT_TIME
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import Platform
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.event import async_track_point_in_utc_time

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entity import StarlingHomeHubEntity
from custom_components.starling_home_hub.integrations import (StarlingHomeHubBinarySensorEntityDescription,
                                                              StarlingHomeHubSwitchEntityDescription)
from custom_components.starling_home_hub.models.api.stream import StartStream

PLACEHOLDER = Path(__file__).parent / "placeholder.png"
STREAM_EXPIRATION_BUFFER = timedelta(seconds=60)

CAMERA_PLATFORMS = {
    Platform.BINARY_SENSOR: [
        StarlingHomeHubBinarySensorEntityDescription(
            key="animal_detected",
            name="Animal Detected",
            relevant_fn=lambda device: "animalDetected" in device,
            value_fn=lambda device: device["animalDetected"],
            device_class=BinarySensorDeviceClass.MOTION
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="doorbell_pushed",
            name="Doorbell Pushed",
            relevant_fn=lambda device: "doorbellPushed" in device,
            value_fn=lambda device: device["doorbellPushed"],
            device_class=BinarySensorDeviceClass.OCCUPANCY
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="garage_door_state",
            name="Garage Door",
            relevant_fn=lambda device: "garageDoorState" in device,
            value_fn=lambda device: device["garageDoorState"] == "open",
            device_class=BinarySensorDeviceClass.GARAGE_DOOR
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="motion_detected",
            name="Motion Detected",
            relevant_fn=lambda device: "motionDetected" in device,
            value_fn=lambda device: device["motionDetected"],
            device_class=BinarySensorDeviceClass.MOTION
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="package_delivered",
            name="Package Delivered",
            relevant_fn=lambda device: "packageDelivered" in device,
            value_fn=lambda device: device["packageDelivered"],
            icon="mdi:package-variant-closed"
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="package_retrieved",
            name="Package Retrieved",
            relevant_fn=lambda device: "packageRetrieved" in device,
            value_fn=lambda device: device["packageRetrieved"],
            icon="mdi:package-variant"
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="person_detected",
            name="Person Detected",
            relevant_fn=lambda device: "personDetected" in device,
            value_fn=lambda device: device["personDetected"],
            device_class=BinarySensorDeviceClass.MOTION
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="sound_detected",
            name="Sound Detected",
            relevant_fn=lambda device: "soundDetected" in device,
            value_fn=lambda device: device["soundDetected"],
            device_class=BinarySensorDeviceClass.SOUND
        ),
        StarlingHomeHubBinarySensorEntityDescription(
            key="vehicle_detected",
            name="Vehicle Detected",
            relevant_fn=lambda device: "vehicleDetected" in device,
            value_fn=lambda device: device["vehicleDetected"],
            device_class=BinarySensorDeviceClass.MOTION,
            icon="mdi:car-estate"
        ),
    ],
    Platform.SWITCH: [
        StarlingHomeHubSwitchEntityDescription(
            key="camera_enabled",
            name="Camera Enabled",
            relevant_fn=lambda device: "cameraEnabled" in device,
            value_fn=lambda device: device["cameraEnabled"],
            icon="mdi:camera",
            entity_category=EntityCategory.CONFIG,
            update_field="cameraEnabled",
            device_class=SwitchDeviceClass.SWITCH
        ),
        StarlingHomeHubSwitchEntityDescription(
            key="quiet_time",
            name="Quiet Time",
            relevant_fn=lambda device: "quietTime" in device,
            value_fn=lambda device: device["quietTime"],
            icon="mdi:sleep",
            entity_category=EntityCategory.CONFIG,
            update_field="quietTime",
            device_class=SwitchDeviceClass.SWITCH
        ),
    ]
}


class StarlingHomeHubCamera(StarlingHomeHubEntity, Camera):
    """Starling Home Hub Camera class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator
    ) -> None:
        """Initialize the Camera Sensor class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self._attr_unique_id = f"{device_id}-camera"

        super().__init__(coordinator)
        Camera.__init__(self)

        device = self.get_device()

        self._attr_name = device.properties["name"]
        self._stream: StartStream | None = None
        self._create_stream_url_lock = asyncio.Lock()
        self._stream_refresh_unsub: Callable[[], None] | None = None
        self._attr_is_streaming = False
        self._attr_supported_features = CameraEntityFeature(0)
        self.stream_options[CONF_EXTRA_PART_WAIT_TIME] = 3

        if device.properties["supportsStreaming"]:
            self._attr_is_streaming = True
            self._attr_supported_features |= CameraEntityFeature.STREAM

    @property
    def use_stream_for_stills(self) -> bool:
        """Whether or not to use stream to generate stills."""

        device = self.get_device()
        supports_streaming = device.properties["supportsStreaming"]
        LOGGER.debug(f"supports streaming: {supports_streaming}")

        return supports_streaming

    @property
    def available(self) -> bool:
        """Return True if entity is available."""

        # Cameras are marked unavailable on stream errors in #54659 however nest
        # streams have a high error rate (#60353). Given nest streams are so flaky,
        # marking the stream unavailable has other side effects like not showing
        # the camera image which sometimes are still able to work. Until the
        # streams are fixed, just leave the streams as available.

        return True

    @property
    def frontend_stream_type(self) -> StreamType | None:
        """Return the type of stream supported by this camera."""

        device = self.get_device()
        if device.properties["supportsStreaming"]:
            return StreamType.WEB_RTC
        else:
            return None

    async def stream_source(self) -> str | None:
        """Return stream source for the camera."""

        return None

    def _schedule_stream_refresh(self) -> None:
        """Schedules an alarm to refresh the stream url before expiration."""

        if not self._stream:
            return

        refresh_time = datetime.now(timezone.utc) + STREAM_EXPIRATION_BUFFER
        LOGGER.debug("New stream url expires at %s", refresh_time)

        if self._stream_refresh_unsub is not None:
            self._stream_refresh_unsub()

        self._stream_refresh_unsub = async_track_point_in_utc_time(
            self.hass,
            self._handle_stream_refresh,
            refresh_time,
        )

    async def _handle_stream_refresh(self, now: datetime) -> None:
        """Alarm that fires to check if the stream should be refreshed."""

        if not self._stream:
            return

        try:
            await self.coordinator.extend_stream(self.device_id, self._stream.streamId)
        except Exception as err:
            LOGGER.debug("Failed to extend stream: %s", err)
            self._stream = None
            if self.stream:
                await self.stream.stop()
                self.stream = None
            return

        self._schedule_stream_refresh()

    async def async_will_remove_from_hass(self) -> None:
        """Invalidate the RTSP token when unloaded."""

        if self._stream:
            LOGGER.debug("Invalidating stream")
            await self.coordinator.stop_stream(self.device_id, self._stream.streamId)

        if self._stream_refresh_unsub:
            self._stream_refresh_unsub()

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""

        return await self.hass.async_add_executor_job(self.placeholder_image)

    async def async_handle_web_rtc_offer(self, offer_sdp: str) -> str | None:
        """Return the source of the stream."""

        device = self.get_device()

        if not device.properties["supportsStreaming"]:
            return await super().async_handle_web_rtc_offer(offer_sdp)

        self._stream = await self.coordinator.start_stream(device_id=self.device_id, sdp_offer=offer_sdp)
        self._schedule_stream_refresh()

        return self.decode_stream_answer(self._stream.answer)

    def decode_stream_answer(self, stream_answer: str) -> str:
        """Decode the stream RTC offer back to a string."""

        return base64.decodebytes(stream_answer.encode()).decode()

    @classmethod
    @functools.cache
    def placeholder_image(cls) -> bytes:
        """Return placeholder image to use when no stream is available."""
        return PLACEHOLDER.read_bytes()
