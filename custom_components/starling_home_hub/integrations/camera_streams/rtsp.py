"""Specific code for RTSP camera streams."""

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.integrations.camera_streams.base import StarlingHomeHubBaseCamera


class StarlingHomeHubRTSPCamera(StarlingHomeHubBaseCamera):
    """Starling Home Hub RTSP Camera class."""

    _rtsp_username: str | None
    _rtsp_password: str | None

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        rtsp_username: str = None,
        rtsp_password: str = None
    ) -> None:
        """Initialize the Camera RTSP class."""

        self._rtsp_username = rtsp_username
        self._rtsp_password = rtsp_password

        super().__init__(device_id, coordinator, "rtsp")

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        url = self.get_device().properties["rtspUrl"]

        if self._rtsp_username and self._rtsp_password:
            url = url.replace(
                "rtsp://", f"rtsp://{self._rtsp_username}:{self._rtsp_password}@")

        return url
