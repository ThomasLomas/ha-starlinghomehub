"""Specific code for WebRTC camera streams."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from webrtc_models import RTCIceCandidate

from homeassistant.components.camera import WebRTCAnswer, WebRTCClientConfiguration, WebRTCSendMessage
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_point_in_utc_time

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities.camera import StarlingHomeHubBaseCamera
from custom_components.starling_home_hub.models.api.stream import StartStream

STREAM_EXPIRATION_BUFFER = timedelta(seconds=60)


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
            LOGGER.debug("Stopping stream")
            try:
                await self.coordinator.stop_stream(self.device_id, self._stream.streamId)
            except Exception as err:
                LOGGER.warning("Failed to stop stream: %s", err)

        if self._stream_refresh_unsub:
            self._stream_refresh_unsub()

        self._stream = None

    async def async_on_webrtc_candidate(
        self, session_id: str, candidate: RTCIceCandidate
    ) -> None:
        """Ignore WebRTC candidates for Nest cloud based cameras."""
        return

    @callback
    def close_webrtc_session(self, session_id: str) -> None:
        """Close a WebRTC session."""

        if self._stream:
            LOGGER.debug("Stopping stream")

            async def stop_stream() -> None:
                try:
                    await self.coordinator.stop_stream(self.device_id, self._stream.streamId)
                except Exception as err:
                    LOGGER.warning("Failed to stop stream: %s", err)

            self.hass.async_create_task(stop_stream())

        if self._stream_refresh_unsub:
            self._stream_refresh_unsub()

        self._stream = None

    async def async_handle_async_webrtc_offer(
        self, offer_sdp: str, session_id: str, send_message: WebRTCSendMessage
    ) -> None:
        """Handle an async WebRTC offer from the frontend."""

        if not self._stream:
            self._stream = await self.coordinator.start_stream(device_id=self.device_id, sdp_offer=offer_sdp)
            self._schedule_stream_refresh()

        send_message(WebRTCAnswer(self._stream.answer))

    @callback
    def _async_get_webrtc_client_configuration(self) -> WebRTCClientConfiguration:
        """Create data channel required for an acceptable WebRTC offer."""
        return WebRTCClientConfiguration(data_channel="dataSendChannel")
