"""DataUpdateCoordinator for starling_home_hub."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    StarlingHomeHubApiClient,
    StarlingHomeHubApiClientAuthenticationError,
    StarlingHomeHubApiClientError,
)
from .const import DOMAIN, LOGGER
from .models import CoordinatorData, SpecificDevice

# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class StarlingHomeHubDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    data: CoordinatorData

    def __init__(
        self,
        hass: HomeAssistant,
        client: StarlingHomeHubApiClient,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.client = client

    async def fetch_data(self) -> CoordinatorData:
        """Fetch data for the devices"""
        devices = await self.client.async_get_devices()
        status = await self.client.async_get_status()

        full_devices: dict[str, SpecificDevice] = {}
        for device in devices:
            full_device = await self.client.async_get_device(device_id=device["id"])
            full_devices[device["id"]] = full_device

        self.data = CoordinatorData(devices=full_devices, status=status)

        return self.data

    async def _async_update_data(self) -> CoordinatorData:
        """Update data via library."""
        try:
            return await self.fetch_data()
        except StarlingHomeHubApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except StarlingHomeHubApiClientError as exception:
            raise UpdateFailed(exception) from exception
