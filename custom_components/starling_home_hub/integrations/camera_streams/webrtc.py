"""Specific code for WebRTC camera streams."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import datetime, timezone

from homeassistant.components.camera import StreamType
from homeassistant.helpers.event import async_track_point_in_utc_time

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.integrations.camera_streams.base import StarlingHomeHubBaseCamera
from custom_components.starling_home_hub.integrations.camera_streams.const import STREAM_EXPIRATION_BUFFER
from custom_components.starling_home_hub.models.api.stream import StartStream


class StarlingHomeHubWebRTCCamera(StarlingHomeHubBaseCamera):
    """Starling Home Hub Web RTC Camera class (Work in progress)."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator
    ) -> None:
        """Initialize the Camera Sensor class."""

        self._stream: StartStream | None = None
        self._create_stream_url_lock = asyncio.Lock()
        self._stream_refresh_unsub: Callable[[], None] | None = None

        super().__init__(device_id, coordinator, "webrtc")

    @property
    def frontend_stream_type(self) -> StreamType | None:
        """Return the type of stream supported by this camera."""

        return StreamType.WEB_RTC

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

    async def async_handle_web_rtc_offer(self, offer_sdp: str) -> str | None:
        """Return the source of the stream."""

        device = self.get_device()

        if not device.properties["supportsStreaming"]:
            return await super().async_handle_web_rtc_offer(offer_sdp)

        self._stream = await self.coordinator.start_stream(device_id=self.device_id, sdp_offer=offer_sdp)
        self._schedule_stream_refresh()

        return self._stream.answer
