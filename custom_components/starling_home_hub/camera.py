"""Camera platform for Starling Home Hub."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.starling_home_hub.const import DOMAIN
from custom_components.starling_home_hub.integrations.camera import StarlingHomeHubCamera
from custom_components.starling_home_hub.models.coordinator import CoordinatorData


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the camera platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[StarlingHomeHubCamera] = []
    data: CoordinatorData = coordinator.data

    for device in filter(lambda device: device[1].properties["type"] == "camera", data.devices.items()):
        entities.append(
            StarlingHomeHubCamera(
                device_id=device[0],
                coordinator=coordinator
            )
        )

    async_add_entities(entities, True)
