"""Purifier Platform"""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo airQuality, fanSpeed, filterChangeIndication, isDocked, isOn, mode
PURIFIER_PLATFORMS = from_base_entities()
