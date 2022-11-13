"""DataUpdateCoordinator for the IMA Protect Alarm integration."""
from __future__ import annotations

from datetime import timedelta
from http import HTTPStatus
from pyimaprotect import IMAProtect
from pyimaprotect import IMAProtectConnectError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import Event
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import Throttle

from .const import DEFAULT_SCAN_INTERVAL
from .const import DOMAIN
from .const import LOGGER


class IMAProtectDataUpdateCoordinator(DataUpdateCoordinator):
    """A IMA Protect Alarm Data Update Coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the IMA Protect Alarm."""
        self.imageseries = {}
        self.entry = entry

        self.imaprotect = IMAProtect(
            username=entry.data[CONF_EMAIL], password=entry.data[CONF_PASSWORD]
        )

        super().__init__(
            hass, LOGGER, name=DOMAIN, update_interval=DEFAULT_SCAN_INTERVAL
        )

    async def async_login(self) -> bool:
        """Login to IMA Protect Alarm."""
        try:
            await self.hass.async_add_executor_job(self.imaprotect.login)
        except IMAProtectConnectError as ex:
            LOGGER.error("Could not log in to IMA Protect Alarm, %s", ex)
            return False

        return True

    async def async_logout(self, _event: Event) -> bool:
        """Logout from IMA Protect Alarm."""
        try:
            await self.hass.async_add_executor_job(self.imaprotect.logout)
        except IMAProtectConnectError as ex:
            LOGGER.error("Could not log out from IMA Protect Alarm, %s", ex)
            return False
        return True

    async def _async_update_data(self) -> dict:
        """Fetch data from IMA Protect Alarm."""
        try:
            status = await self.hass.async_add_executor_job(
                self.imaprotect.__getattribute__, "status"
            )
            cameralist = await self.hass.async_add_executor_job(
                self.imaprotect._capture_list
            )
        except IMAProtectConnectError as ex:
            LOGGER.error("Could not read overview, %s", ex)
            if ex.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
                LOGGER.info("Trying to log in again")
                await self.async_login()
                return {}
            raise

        # Store data in a way Home Assistant can easily consume it
        return {
            "alarm": status,
            "cameras": cameralist,
        }

    @Throttle(timedelta(seconds=60))
    def update_smartcam_imageseries(self) -> None:
        """Update the image series."""
        self.imageseries = self.imaprotect._capture_list()
