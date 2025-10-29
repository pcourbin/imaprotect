"""Config flow for IMA Protect Alarm integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import ConfigFlow
from homeassistant.config_entries import OptionsFlow
from homeassistant.const import CONF_EMAIL
from homeassistant.const import CONF_NAME
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)

from pyimaprotect import IMAProtect
from pyimaprotect import IMAProtectConnectError

from .const import CONF_ALARM_CODE
from .const import CONF_IMA_CONTRACT_NUM
from .const import CONF_SELENIUM_WEBDRIVER
from .const import DOMAIN
from .const import LOGGER


class IMAProtectConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IMA Protect Alarm."""

    VERSION = 1

    email: str
    entry: ConfigEntry
    password: str
    name: str
    selenium_webdriver: str
    ima_contract_num: str | None
    imaprotect: IMAProtect

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> IMAProtectOptionsFlowHandler:
        """Get the options flow for this handler."""
        return IMAProtectOptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            local_ima_contract_num = user_input[CONF_IMA_CONTRACT_NUM]
            if (local_ima_contract_num == ""):
                local_ima_contract_num = None
            self.imaprotect = IMAProtect(
                username=user_input[CONF_EMAIL], password=user_input[CONF_PASSWORD], remote_webdriver=user_input[CONF_SELENIUM_WEBDRIVER], contract_number=local_ima_contract_num
            )
            try:
                await self.hass.async_add_executor_job(self.imaprotect.login)
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
                self.selenium_webdriver = user_input[CONF_SELENIUM_WEBDRIVER]
                self.ima_contract_num = user_input[CONF_IMA_CONTRACT_NUM]
                if (self.ima_contract_num == ""):
                    self.ima_contract_num = None

                return await self.async_step_installation()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_SELENIUM_WEBDRIVER, default="http://localhost:4444"): str,
                    vol.Optional(CONF_IMA_CONTRACT_NUM, default=""): str,
                }
            ),
            errors=errors,
        )

    async def async_step_installation(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Select IMA Protect Alarm installation to add."""

        await self.async_set_unique_id(self.name)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=self.name,
            data={
                CONF_NAME: self.name,
                CONF_EMAIL: self.email,
                CONF_PASSWORD: self.password,
                CONF_SELENIUM_WEBDRIVER: self.selenium_webdriver,
                CONF_IMA_CONTRACT_NUM: self.ima_contract_num,
            },
        )

    async def async_step_reauth(self, data: dict[str, Any]) -> ConfigFlowResult:
        """Handle initiation of re-authentication with IMA Protect Alarm."""
        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle re-authentication with IMA Protect Alarm."""
        errors: dict[str, str] = {}

        if user_input is not None:
            local_ima_contract_num = user_input[CONF_IMA_CONTRACT_NUM]
            if (local_ima_contract_num == ""):
                local_ima_contract_num = None
            self.imaprotect = IMAProtect(
                username=user_input[CONF_EMAIL], password=user_input[CONF_PASSWORD], remote_webdriver=user_input[CONF_SELENIUM_WEBDRIVER], contract_number=local_ima_contract_num
            )
            try:
                await self.hass.async_add_executor_job(self.imaprotect.login)
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
                        CONF_SELENIUM_WEBDRIVER: user_input[CONF_SELENIUM_WEBDRIVER],
                        CONF_IMA_CONTRACT_NUM: local_ima_contract_num,
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
                    vol.Required(CONF_SELENIUM_WEBDRIVER, default=self.entry.data[CONF_SELENIUM_WEBDRIVER]): str,
                    vol.Optional(CONF_IMA_CONTRACT_NUM, default=self.entry.data[CONF_IMA_CONTRACT_NUM]): str | None,
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
    ) -> ConfigFlowResult:
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
