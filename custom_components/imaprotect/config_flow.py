"""Config flow for IMA Protect Alarm integration."""
from __future__ import annotations

from pyimaprotect import IMAProtect
from pyimaprotect import IMAProtectConnectError
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import ConfigFlow
from homeassistant.config_entries import OptionsFlow
from homeassistant.const import CONF_EMAIL
from homeassistant.const import CONF_NAME
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_ALARM_CODE
from .const import DOMAIN
from .const import LOGGER


class IMAProtectConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IMA Protect Alarm."""

    VERSION = 1

    email: str
    entry: ConfigEntry
    password: str
    name: str

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> IMAProtectOptionsFlowHandler:
        """Get the options flow for this handler."""
        return IMAProtectOptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            imaprotect = IMAProtect(
                username=user_input[CONF_EMAIL], password=user_input[CONF_PASSWORD]
            )
            try:
                await self.hass.async_add_executor_job(imaprotect.login)
            except IMAProtectConnectError as ex:
                LOGGER.debug("Could not log in to IMA Protect Alarm, %s", ex)
                errors["base"] = "invalid_auth"
            except Exception as ex:
                LOGGER.debug("Unexpected response from IMA Protect Alarm, %s", ex)
                errors["base"] = "unknown"
            else:
                self.email = user_input[CONF_EMAIL]
                self.password = user_input[CONF_PASSWORD]
                self.name = user_input[CONF_NAME]

                return await self.async_step_installation()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    async def async_step_installation(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Select IMA Protect Alarm installation to add."""

        await self.async_set_unique_id(self.name)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=self.name,
            data={
                CONF_NAME: self.name,
                CONF_EMAIL: self.email,
                CONF_PASSWORD: self.password,
            },
        )

    async def async_step_reauth(self, data: dict[str, Any]) -> FlowResult:
        """Handle initiation of re-authentication with IMA Protect Alarm."""
        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle re-authentication with IMA Protect Alarm."""
        errors: dict[str, str] = {}

        if user_input is not None:
            imaprotect = IMAProtect(
                username=user_input[CONF_EMAIL], password=user_input[CONF_PASSWORD]
            )
            try:
                await self.hass.async_add_executor_job(imaprotect.login)
            except IMAProtectConnectError as ex:
                LOGGER.debug("Could not log in to IMA Protect Alarm, %s", ex)
                errors["base"] = "invalid_auth"
            except Exception as ex:
                LOGGER.debug("Unexpected response from IMA Protect Alarm, %s", ex)
                errors["base"] = "unknown"
            else:
                data = self.entry.data.copy()
                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data={
                        **data,
                        CONF_EMAIL: user_input[CONF_EMAIL],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                    },
                )
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self.entry.entry_id)
                )
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL, default=self.entry.data[CONF_EMAIL]): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )


class IMAProtectOptionsFlowHandler(OptionsFlow):
    """Handle IMA Protect Alarm options."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize IMA Protect Alarm options flow."""
        self.entry = entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage IMA Protect Alarm options."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_ALARM_CODE,
                        default=self.entry.options.get(CONF_ALARM_CODE, ""),
                    ): str,
                }
            ),
            errors=errors,
        )
