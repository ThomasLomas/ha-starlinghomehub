"""Loader for Starling Home Hub entities."""

from dataclasses import dataclass
from typing import Callable

from homeassistant.const import Platform
from homeassistant.helpers.entity import Entity

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.integrations import ENTITY_DESCRIPTION_TYPES, StarlingHomeHubEntityDescriptionFactory
from custom_components.starling_home_hub.integrations.const import DEVICE_CATEGORIES_TO_PLATFORMS
from custom_components.starling_home_hub.models.api.device import Device


@dataclass
class DeviceEntityDescription:
    """Couples a device with an entity description."""

    device: Device
    entity_description: ENTITY_DESCRIPTION_TYPES


def load_entities_for_platform(coordinator: StarlingHomeHubDataUpdateCoordinator, platform: Platform, createEntity: Callable[[DeviceEntityDescription], Entity]) -> list[Entity]:
    """Load entities for the platform."""

    entities: list[Entity] = []

    for device in coordinator.data.devices.values():
        category = device.properties["category"]
        if platform in DEVICE_CATEGORIES_TO_PLATFORMS.get(category, {}):
            for entity_description in DEVICE_CATEGORIES_TO_PLATFORMS[category][platform]:
                descriptions = (entity_description.entities(device.properties)
                                if isinstance(entity_description, StarlingHomeHubEntityDescriptionFactory)
                                else [entity_description])
                for desc in descriptions:
                    if not desc.relevant_fn or desc.relevant_fn(device.properties):
                        entities.append(createEntity(DeviceEntityDescription(
                            device=device, entity_description=desc)))

    return entities
