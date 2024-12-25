"""Integrations for the fan control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# Fan specific platforms handled directly in StarlingHomeHubFanEntity
FAN_PLATFORMS = from_base_entities()
