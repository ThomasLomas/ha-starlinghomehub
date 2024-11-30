"""Support for Starling Home Hub lights."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.integrations.light import StarlingHomeHubLightEntity
from custom_components.starling_home_hub.models.coordinator import CoordinatorData


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the light platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    data: CoordinatorData = coordinator.data

    entities = [
        StarlingHomeHubLightEntity(
            device_id=device_id, coordinator=coordinator)
        for device_id, device in data.devices.items()
        if device.properties["type"] == "light"
    ]

    async_add_entities(entities, True)
