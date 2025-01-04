"""Support for Starling Home Hub lights."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.entities.light import StarlingHomeHubLightEntity
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator, StarlingHomeHubConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: StarlingHomeHubConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the light platform."""

    coordinator: StarlingHomeHubDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubLightEntity] = []

    for device in filter(lambda device: device[1].properties["type"] == "light" or device[1].properties["category"] == "diffuser", entry.runtime_data.devices.items()):
        entities.append(
            StarlingHomeHubLightEntity(
                device_id=device[0],
                coordinator=coordinator
            )
        )

    async_add_entities(entities, update_before_add=True)
