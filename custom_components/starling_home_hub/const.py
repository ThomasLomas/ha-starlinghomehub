"""All constants used globally across the integration."""

from logging import Logger, getLogger

from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

NAME = "Starling Home Hub Integration"
DOMAIN = "starling_home_hub"
VERSION = "1.7.0"
ATTRIBUTION = "Based on the Starling Home Hub Developer Connect API"

CONF_ENABLE_RTSP_STREAM = "enable_rtsp_stream"
CONF_ENABLE_WEBRTC_STREAM = "enable_webrtc_stream"
CONF_RTSP_USERNAME = "rtsp_username"
CONF_RTSP_PASSWORD = "rtsp_password"

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.CAMERA,
    Platform.SELECT,
    Platform.FAN,
    Platform.LOCK,
    Platform.COVER,
    Platform.VALVE,
    Platform.VACUUM,
    Platform.LIGHT,
]
