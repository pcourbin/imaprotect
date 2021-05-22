"""Support for IMA Protect alarm control panels."""
from __future__ import annotations

import asyncio
import re

from homeassistant.components.alarm_control_panel import (
    FORMAT_NUMBER,
    FORMAT_TEXT,
    AlarmControlPanelEntity,
)
from homeassistant.components.alarm_control_panel.const import (
    SUPPORT_ALARM_ARM_AWAY,
    SUPPORT_ALARM_ARM_HOME,
)
from homeassistant.const import CONF_NAME, ATTR_CODE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ALARM_STATE_TO_HA, DOMAIN, LOGGER, CONF_ALARM_CODE, LOGGER
from .coordinator import IMAProtectDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up IMA Protect alarm control panel from a config entry."""
    async_add_entities([IMAProtectAlarm(coordinator=hass.data[DOMAIN][entry.entry_id])])


class IMAProtectAlarm(CoordinatorEntity, AlarmControlPanelEntity):
    """Representation of a IMAProtect alarm status."""

    coordinator: IMAProtectDataUpdateCoordinator

    _changed_by: str | None = None
    _state: str | None = None

    def __init__(
        self, coordinator: IMAProtectDataUpdateCoordinator
    ) -> None:
        """Initialize the IMA Protect Alarm Control Panel."""
        super().__init__(coordinator)
        self._changed_by = None
        self._state = None

    @property
    def code(self):
        return self.coordinator.entry.options.get(CONF_ALARM_CODE)

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self.coordinator.entry.data[CONF_NAME]

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this entity."""
        return self.coordinator.entry.data[CONF_NAME]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return {
            "name": "IMA Protect Alarm",
            "manufacturer": "IMA International",
            "model": "",
            "identifiers": {(DOMAIN, self.coordinator.entry.data[CONF_NAME])},
        }

    @property
    def state(self) -> str | None:
        """Return the state of the entity."""
        return self._state

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_ALARM_ARM_HOME | SUPPORT_ALARM_ARM_AWAY

    @property
    def code_format(self):
        code = self.code
        if code is None or code == "":
            return None
        if isinstance(code, str) and re.search("^\\d+$", code):
            return FORMAT_NUMBER
        return FORMAT_TEXT

    @property
    def changed_by(self) -> str | None:
        """Return the last change triggered by."""
        return self._changed_by

    def _validate_code(self, code_test) -> bool:
        code = self.code
        if code is None or code == "":
            return True
        if isinstance(code, str):
            alarm_code = code
        else:
            alarm_code = code.render(parse_result=False)
        check = not alarm_code or code_test == alarm_code
        if not check:
            LOGGER.warning("Invalid code given")
        return check

    async def _async_set_arm_state(self, state: int, code = None) -> None:
        """Send set arm state command."""
        if not self._validate_code(code):
            return

        await self.hass.async_add_executor_job(
            self.coordinator.imaprotect.__setattr__, "status", state
        )
        LOGGER.debug("IMA Protect set arm state %s", state)
        await self.coordinator.async_refresh()

    async def async_alarm_disarm(self, code = None) -> None:
        """Send disarm command."""
        await self._async_set_arm_state(0, code)

    async def async_alarm_arm_home(self, code = None) -> None:
        """Send arm home command."""
        await self._async_set_arm_state(1, code)

    async def async_alarm_arm_away(self, code = None) -> None:
        """Send arm away command."""
        await self._async_set_arm_state(2, code)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._state = ALARM_STATE_TO_HA.get(
            self.coordinator.data["alarm"]
        )
        self._changed_by = "Not Implemented" # TODO: self.coordinator.data["alarm"].get("name")
        super()._handle_coordinator_update()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()