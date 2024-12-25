"""Integrations for the light control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo: brightness, colorTemperature, hue, isOn, saturation
LIGHT_PLATFORMS = from_base_entities()
