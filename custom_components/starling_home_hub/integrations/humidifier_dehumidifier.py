"""Integrations for the humidifer/dehumidifer control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo: canHumidify, canDehumidify, currentTemperature, fanSpeed, humidityPercent, isOn, maxTargetHumidity, minTargetHumidity, state, targetHumidity
HUMIDIFIER_DEHUMIDIFIER_PLATFORMS = from_base_entities()
