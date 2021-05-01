"""Config flow to configure the imaprotect integration."""
from pyimaprotect import IMAProtect

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME

from .const import (
    DOMAIN,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default="IMA Protect Alarm"): str,
        vol.Optional(CONF_USERNAME): str,
        vol.Optional(CONF_PASSWORD): str,
    }
)


@config_entries.HANDLERS.register(DOMAIN)
class IMAProtectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a imaprotect config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_import(self, user_input=None):
        """Handle configuration by yaml file."""
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            entry = await self.async_set_unique_id(
                f"{DOMAIN}, {user_input.get(CONF_NAME)}"
            )

            if entry:
                self.hass.config_entries.async_update_entry(entry, data=user_input)
                self._abort_if_unique_id_configured()

            controller = IMAProtect(
                user_input.get(CONF_USERNAME),
                user_input.get(CONF_PASSWORD),
            )

            testconnect = await self.hass.async_add_executor_job(
                controller.get_all_info
            )
            if testconnect[0]["pk"] != 0:
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME), data=user_input
                )

            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
