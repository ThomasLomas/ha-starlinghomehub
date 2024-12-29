"""Starling Home Hub Developer Connect API Client."""

from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout
from homeassistant.exceptions import HomeAssistantError

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.models.api.device import Device, DeviceUpdate
from custom_components.starling_home_hub.models.api.devices import Devices
from custom_components.starling_home_hub.models.api.status import Status
from custom_components.starling_home_hub.models.api.stream import StartStream, StreamStatus


class StarlingHomeHubApiClientError(Exception):
    """Exception to indicate a general API error."""


class StarlingHomeHubApiClientCommunicationError(
    StarlingHomeHubApiClientError
):
    """Exception to indicate a communication error."""


class StarlingHomeHubApiClientAuthenticationError(
    StarlingHomeHubApiClientError
):
    """Exception to indicate an authentication error."""


class StarlingHomeHubApiClient:
    """Starling Home Hub Developer Connect API Client."""

    def __init__(
        self,
        url: str,
        api_key: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Starling Home Hub Developer Connect API Client."""
        self._url = url
        self._api_key = api_key
        self._session = session

    def get_api_url_for_endpoint(self, endpoint: str) -> str:
        """Build URL for the API."""
        return self._url + endpoint + "?key=" + self._api_key

    async def async_get_status(self) -> Status:
        """Get status from the API."""
        status_response = await self._api_wrapper(
            method="get", url=self.get_api_url_for_endpoint("status")
        )

        return Status.create_from_dict(status_response)

    async def async_get_device(self, device_id: str) -> Device:
        """Get devices from the API."""
        device_response = await self._api_wrapper(
            method="get", url=self.get_api_url_for_endpoint(f"devices/{device_id}")
        )

        return Device(**device_response)

    async def async_update_device(self, device_id: str, update: dict) -> DeviceUpdate:
        """Update a device."""
        LOGGER.debug(f"Updating device {device_id} with {update}")

        update_response = await self._api_wrapper(
            method="post",
            url=self.get_api_url_for_endpoint(f"devices/{device_id}"),
            data=update,
            headers={"Content-type": "application/json; charset=UTF-8"}
        )

        LOGGER.debug(f"Response from update: {update_response}")

        device_update = DeviceUpdate(**update_response)

        if device_update.setStatus:
            # Loop all the set status results and check if any errors
            for key, value in device_update.setStatus.items():
                if value == "READ_ONLY_PROPERTY":
                    raise HomeAssistantError(
                        f"Error setting {key}: Failed - property is read-only")
                elif value == "INVALID_VALUE":
                    raise HomeAssistantError(
                        f"Error setting {key}: Failed - property value specified is invalid")
                elif value == "PROPERTY_NOT_FOUND":
                    raise HomeAssistantError(
                        f"Error setting {key}: Failed - property specified does not exist")
                elif value == "SET_ERROR":
                    raise HomeAssistantError(
                        f"Error setting {key}: Failed - the Google Home service reported an error trying to set the property")

        return device_update

    async def async_get_devices(self) -> list[Device]:
        """Get devices from the API."""
        devices_response = await self._api_wrapper(
            method="get", url=self.get_api_url_for_endpoint("devices")
        )

        return Devices(**devices_response).devices

    async def async_start_stream(self, device_id: str, sdp_offer: str) -> StartStream:
        """Start a WebRTC Stream."""
        data = {"offer": sdp_offer}
        LOGGER.debug(f"Starting stream for device {
            device_id}")

        start_stream_response = await self._api_wrapper(
            method="post",
            url=self.get_api_url_for_endpoint(f"devices/{device_id}/stream"),
            data=data,
            headers={"Content-type": "application/json; charset=UTF-8"}
        )

        LOGGER.debug(f"Response from start stream: {start_stream_response}")

        return StartStream(**start_stream_response)

    async def async_stop_stream(self, device_id: str, stream_id: str) -> StreamStatus:
        """Stop a WebRTC Stream."""
        stop_stream_response = await self._api_wrapper(
            method="post",
            url=self.get_api_url_for_endpoint(
                f"devices/{device_id}/stream/{stream_id}/stop"),
            headers={"Content-type": "application/json; charset=UTF-8"},
            data={}
        )

        return StreamStatus(**stop_stream_response)

    async def async_get_camera_snapshot(self, device_id: str) -> bytes:
        """Get a camera snapshot."""
        return await self._api_wrapper(
            method="get",
            url=self.get_api_url_for_endpoint(
                f"devices/{device_id}/snapshot"),
            as_json=False
        )

    async def async_extend_stream(self, device_id: str, stream_id: str) -> StreamStatus:
        """Extend a WebRTC Stream."""
        extend_stream_response = await self._api_wrapper(
            method="post",
            url=self.get_api_url_for_endpoint(
                f"devices/{device_id}/stream/{stream_id}/extend"),
            headers={"Content-type": "application/json; charset=UTF-8"},
            data={}
        )

        return StreamStatus(**extend_stream_response)

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
        as_json: bool = True,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise StarlingHomeHubApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json() if as_json else await response.read()

        except asyncio.TimeoutError as exception:
            raise StarlingHomeHubApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise StarlingHomeHubApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except StarlingHomeHubApiClientAuthenticationError as exception:
            raise exception
        except Exception as exception:  # pylint: disable=broad-except
            raise StarlingHomeHubApiClientError(
                "Something really wrong happened!"
            ) from exception
