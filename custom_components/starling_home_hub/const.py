"""Constants for starling_home_hub."""
from logging import Logger, getLogger

from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

NAME = "Starling Home Hub Integration"
DOMAIN = "starling_home_hub"
VERSION = "0.0.0"
ATTRIBUTION = "Based on the Starling Home Hub Developer Connect API"

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.CAMERA
]
