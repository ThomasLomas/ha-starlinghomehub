"""Starling Home Hub Developer Connect API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


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

    async def async_get_status(self) -> any:
        """Get status from the API."""
        return await self._api_wrapper(
            method="get", url=self.get_api_url_for_endpoint("status")
        )

    async def async_set_title(self, value: str) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
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
                return await response.json()

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
