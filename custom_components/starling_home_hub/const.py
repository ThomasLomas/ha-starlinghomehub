"""All constants used globally across the integration."""

from logging import Logger, getLogger

from homeassistant.const import Platform

from custom_components.starling_home_hub.integrations.sensor import SENSOR_PLATFORMS
from custom_components.starling_home_hub.integrations.smoke_detector import SMOKE_DETECTOR_PLATFORMS

LOGGER: Logger = getLogger(__package__)

NAME = "Starling Home Hub Integration"
DOMAIN = "starling_home_hub"
VERSION = "1.0.3"
ATTRIBUTION = "Based on the Starling Home Hub Developer Connect API"

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    # Platform.CAMERA,
]

DEVICE_TYPES_TO_PLATFORMS = {
    "smoke_detector": SMOKE_DETECTOR_PLATFORMS,
    "sensor": SENSOR_PLATFORMS,
}
