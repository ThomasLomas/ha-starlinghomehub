"""Custom integration to integrate starling_home_hub with Home Assistant.

For more details about this integration, please refer to
https://github.com/ThomasLomas/ha-starlinghomehub
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntry

from custom_components.starling_home_hub.api import StarlingHomeHubApiClient
from custom_components.starling_home_hub.const import DOMAIN, LOGGER, PLATFORMS
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""

    client = StarlingHomeHubApiClient(
        url=entry.data[CONF_URL],
        api_key=entry.data[CONF_API_KEY],
        session=async_get_clientsession(hass),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = StarlingHomeHubDataUpdateCoordinator(
        hass=hass,
        client=client,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Remove a config entry from a device."""
    LOGGER.info(f"Removing device {device_entry.serial_number}")

    coordinator: StarlingHomeHubDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    starling_device_id = list(device_entry.identifiers)[0][1]

    if starling_device_id in coordinator.data.devices:
        LOGGER.warning(f"Not removing device {
                       starling_device_id} - still in use")
        return False

    return True
