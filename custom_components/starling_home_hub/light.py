"""Support for Starling Home Hub lights."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.entities.light import StarlingHomeHubLightEntity
from custom_components.starling_home_hub.models.coordinator import CoordinatorData


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the light platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubLightEntity] = []
    data: CoordinatorData = coordinator.data

    for device in filter(lambda device: device[1].properties["type"] == "light" or device[1].properties["category"] == "diffuser", data.devices.items()):
        entities.append(
            StarlingHomeHubLightEntity(
                device_id=device[0],
                coordinator=coordinator
            )
        )

    async_add_entities(entities, True)
