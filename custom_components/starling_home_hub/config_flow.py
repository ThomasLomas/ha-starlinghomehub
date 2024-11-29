"""Adds config flow for Staring Home Hub used in initial setup."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from custom_components.starling_home_hub.api import (StarlingHomeHubApiClient, StarlingHomeHubApiClientAuthenticationError,
                                                     StarlingHomeHubApiClientCommunicationError, StarlingHomeHubApiClientError)
from custom_components.starling_home_hub.const import (CONF_ENABLE_RTSP_STREAM, CONF_ENABLE_WEBRTC_STREAM, CONF_RTSP_PASSWORD,
                                                       CONF_RTSP_USERNAME, DOMAIN, LOGGER)


class StarlingHomeHubFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Staring Home Hub."""

    VERSION = 2
    MINOR_VERSION = 0

    def create_schema(self, user_input: dict | None = None) -> vol.Schema:
        """Create schema."""

        return vol.Schema(
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
                vol.Optional(CONF_ENABLE_RTSP_STREAM): bool,
                vol.Optional(CONF_ENABLE_WEBRTC_STREAM): bool,
                vol.Optional(CONF_RTSP_USERNAME): str,
                vol.Optional(CONF_RTSP_PASSWORD): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.PASSWORD
                    ),
                ),
            }
        )

    async def validate_credentials(self, user_input: dict, errors: dict[str, str]) -> dict[str, str]:
        """Validate and populate errors if needed."""

        try:
            await self._test_credentials(
                url=user_input[CONF_URL],
                api_key=user_input[CONF_API_KEY],
            )
        except StarlingHomeHubApiClientAuthenticationError as exception:
            LOGGER.warning(exception)
            errors["base"] = "auth"
        except StarlingHomeHubApiClientCommunicationError as exception:
            LOGGER.error(exception)
            errors["base"] = "connection"
        except StarlingHomeHubApiClientError as exception:
            LOGGER.exception(exception)
            errors["base"] = "unknown"

        return errors

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""

        errors = {}
        if user_input is not None:
            errors = await self.validate_credentials(user_input, errors)

            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_URL],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.create_schema(user_input),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input: dict | None = None) -> config_entries.FlowResult:
        """Handle reconfiguration of existing entry."""

        reconfigure_entry = self._get_reconfigure_entry()
        errors = {}

        LOGGER.debug(f"Reconfiguring entry {reconfigure_entry.data}")

        if user_input is not None:
            LOGGER.debug(f"Updating entry {user_input}")

            errors = await self.validate_credentials(user_input, errors)

            if not errors:
                return self.async_update_reload_and_abort(
                    reconfigure_entry, data_updates=user_input, reload_even_if_entry_is_unchanged=False
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                self.create_schema(user_input), reconfigure_entry.data),
            errors=errors,
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
