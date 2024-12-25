"""Camera platform for Starling Home Hub."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.integrations.camera_rtsp import StarlingHomeHubRTSPCamera
from custom_components.starling_home_hub.integrations.camera_webrtc import StarlingHomeHubWebRTCCamera
from custom_components.starling_home_hub.models.coordinator import CoordinatorData


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the camera platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubWebRTCCamera |
                   StarlingHomeHubRTSPCamera] = []
    data: CoordinatorData = coordinator.data

    enable_rtsp_stream = entry.data.get("enable_rtsp_stream", False)
    # enable_webrtc_stream = entry.data.get("enable_webrtc_stream", False)
    enable_webrtc_stream = False

    for device in filter(lambda device: device[1].properties["category"] == "cam", data.devices.items()):
        if enable_webrtc_stream and "supportsWebRtcStreaming" in device[1].properties and device[1].properties["supportsWebRtcStreaming"]:
            entities.append(
                StarlingHomeHubWebRTCCamera(
                    device_id=device[0],
                    coordinator=coordinator
                )
            )
        elif enable_rtsp_stream and "rtspStreamingEnabled" in device[1].properties and device[1].properties["rtspStreamingEnabled"]:
            entities.append(
                StarlingHomeHubRTSPCamera(
                    device_id=device[0],
                    coordinator=coordinator,
                    rtsp_username=entry.data.get("rtsp_username", None),
                    rtsp_password=entry.data.get("rtsp_password", None)
                )
            )

    async_add_entities(entities, True)
