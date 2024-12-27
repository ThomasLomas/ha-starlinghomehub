"""Integrations for the heater cooler control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo: canCool, canHeat, currentTemperature, fanSpeed, humidityPercent, isOn, mode, state, targetTemperature
HEATER_COOLER_PLATFORMS = from_base_entities()
