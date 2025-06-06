"""Sensor platform for starling_home_hub."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.entities.binary_sensor import StarlingHomeHubBinarySensorEntity
from custom_components.starling_home_hub.integrations import DEVICE_CATEGORIES_TO_PLATFORMS
from custom_components.starling_home_hub.coordinator import StarlingHomeHubConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: StarlingHomeHubConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the binary sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubBinarySensorEntity] = []

    for device in entry.runtime_data.devices.items():
        if device[1].properties["category"] in DEVICE_CATEGORIES_TO_PLATFORMS:
            platforms = DEVICE_CATEGORIES_TO_PLATFORMS[device[1].properties["category"]]
            if Platform.BINARY_SENSOR in platforms:
                entity_descriptions = []

                for entity_description in platforms[Platform.BINARY_SENSOR]:
                    if hasattr(entity_description, "make_entity_descriptions"):
                        entity_descriptions.extend(
                            entity_description.make_entity_descriptions(device[1].properties))
                    else:
                        entity_descriptions.append(entity_description)

                for entity_description in entity_descriptions:
                    if not entity_description.relevant_fn or entity_description.relevant_fn(device[1].properties):
                        entities.append(
                            StarlingHomeHubBinarySensorEntity(
                                device_id=device[0],
                                coordinator=coordinator,
                                entity_description=entity_description
                            )
                        )

    async_add_entities(entities, update_before_add=True)
