"""Sensor platform for starling_home_hub."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entity import StarlingHomeHubBinarySensorEntity
from custom_components.starling_home_hub.integrations.loader import load_entities_for_platform


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the binary sensor platform."""

    coordinator: StarlingHomeHubDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(load_entities_for_platform(
        coordinator, Platform.BINARY_SENSOR, lambda device_entity_description:
            StarlingHomeHubBinarySensorEntity(
                coordinator=coordinator,
                entity_description=device_entity_description.entity_description,
                device_id=device_entity_description.device.properties.get(
                    "id")
            )
    ), True)
