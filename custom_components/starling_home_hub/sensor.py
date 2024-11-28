"""Sensor platform for Starling Home Hub."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.entity import StarlingHomeHubSensorEntity
from custom_components.starling_home_hub.models.coordinator import CoordinatorData

from .const import DEVICE_TYPES_TO_PLATFORMS, DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubSensorEntity] = []
    data: CoordinatorData = coordinator.data

    for device in data.devices.items():
        if device[1].properties["type"] in DEVICE_TYPES_TO_PLATFORMS:
            platforms = DEVICE_TYPES_TO_PLATFORMS[device[1].properties["type"]]
            if Platform.SENSOR in platforms:
                for entity_description in platforms[Platform.SENSOR]:
                    if not entity_description.relevant_fn or entity_description.relevant_fn(device[1].properties):
                        entities.append(
                            StarlingHomeHubSensorEntity(
                                device_id=device[0],
                                coordinator=coordinator,
                                entity_description=entity_description
                            )
                        )

    async_add_entities(entities, True)
