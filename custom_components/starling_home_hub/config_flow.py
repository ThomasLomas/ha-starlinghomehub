"""Adds config flow for Staring Home Hub used in initial setup."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (StarlingHomeHubApiClient, StarlingHomeHubApiClientAuthenticationError, StarlingHomeHubApiClientCommunicationError,
                  StarlingHomeHubApiClientError)
from .const import DOMAIN, LOGGER


class StarlingHomeHubFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Staring Home Hub."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    url=user_input[CONF_URL],
                    api_key=user_input[CONF_API_KEY],
                )
            except StarlingHomeHubApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except StarlingHomeHubApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except StarlingHomeHubApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_URL],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_URL,
                        default=(user_input or {}).get(CONF_URL),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(CONF_API_KEY): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(self, url: str, api_key: str) -> None:
        """Validate credentials."""
        client = StarlingHomeHubApiClient(
            url=url,
            api_key=api_key,
            session=async_create_clientsession(self.hass),
        )

        status_body = await client.async_get_status()

        if not status_body.apiReady:
            raise StarlingHomeHubApiClientCommunicationError(
                "Starling reporting that API is not ready"
            )

        if not status_body.permissions["read"]:
            raise StarlingHomeHubApiClientAuthenticationError(
                "API Key does not have read permissions",
            )
