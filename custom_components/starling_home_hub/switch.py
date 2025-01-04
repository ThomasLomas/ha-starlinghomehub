"""Switch platform for Starling Home Hub."""

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.entities.switch import StarlingHomeHubSwitchEntity
from custom_components.starling_home_hub.integrations import DEVICE_CATEGORIES_TO_PLATFORMS
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator, StarlingHomeHubConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: StarlingHomeHubConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the switch platform."""

    coordinator: StarlingHomeHubDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubSwitchEntity] = []

    for device in entry.runtime_data.devices.items():
        if device[1].properties["category"] in DEVICE_CATEGORIES_TO_PLATFORMS:
            platforms = DEVICE_CATEGORIES_TO_PLATFORMS[device[1].properties["category"]]
            if Platform.SWITCH in platforms:
                for entity_description in platforms[Platform.SWITCH]:
                    if not entity_description.relevant_fn or entity_description.relevant_fn(device[1].properties):
                        entities.append(
                            StarlingHomeHubSwitchEntity(
                                device_id=device[0],
                                coordinator=coordinator,
                                entity_description=entity_description
                            )
                        )

    async_add_entities(entities, update_before_add=True)
