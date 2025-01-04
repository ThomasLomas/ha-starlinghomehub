"""Support for Starling Home Hub thermostats."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.entities.thermostat import StarlingHomeHubThermostatEntity
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator, StarlingHomeHubConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: StarlingHomeHubConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the climate / thermostat platform."""

    coordinator: StarlingHomeHubDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubThermostatEntity] = []

    for device in filter(lambda device: device[1].properties["type"] == "thermostat", entry.runtime_data.devices.items()):
        entities.append(
            StarlingHomeHubThermostatEntity(
                device_id=device[0],
                coordinator=coordinator
            )
        )

    async_add_entities(entities, update_before_add=True)
