"""Select platform for Starling Home Hub."""

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.entities.select import StarlingHomeHubSelectEntity
from custom_components.starling_home_hub.integrations import DEVICE_CATEGORIES_TO_PLATFORMS
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator, StarlingHomeHubConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: StarlingHomeHubConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the select platform."""

    coordinator: StarlingHomeHubDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubSelectEntity] = []

    for device in entry.runtime_data.devices.items():
        if device[1].properties["category"] in DEVICE_CATEGORIES_TO_PLATFORMS:
            platforms = DEVICE_CATEGORIES_TO_PLATFORMS[device[1].properties["category"]]
            if Platform.SELECT in platforms:
                for entity_description in platforms[Platform.SELECT]:
                    if not entity_description.relevant_fn or entity_description.relevant_fn(device[1].properties):
                        entities.append(
                            StarlingHomeHubSelectEntity(
                                device_id=device[0],
                                coordinator=coordinator,
                                entity_description=entity_description
                            )
                        )

    async_add_entities(entities, update_before_add=True)
