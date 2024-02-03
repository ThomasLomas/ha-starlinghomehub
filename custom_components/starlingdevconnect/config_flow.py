"""Adds config flow for starling dev connect."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    StarlingDevConnectApiClient,
    StarlingDevConnectApiClientAuthenticationError,
    StarlingDevConnectApiClientCommunicationError,
    StarlingDevConnectApiClientError,
)
from .const import DOMAIN, LOGGER


class StarlingDevConnectFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for starling dev connect."""

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
            except StarlingDevConnectApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except StarlingDevConnectApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except StarlingDevConnectApiClientError as exception:
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
        client = StarlingDevConnectApiClient(
            url=url,
            api_key=api_key,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
