"""IMA Protect Alarm integration"""
import asyncio
import logging
from pyimaprotect import IMAProtect

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr

from .const import CONFIG
from .const import CONTROLLER
from .const import DOMAIN
from .const import PLATFORMS
from .const import UNDO_UPDATE_LISTENER

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the IMA Protect Alarm integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up IMA Protect Alarm from a config entry."""
    config = entry.data

    controller = IMAProtect(
        config.get(CONF_USERNAME),
        config.get(CONF_PASSWORD),
    )

    testconnect = await hass.async_add_executor_job(controller.get_status)
    try:
        testconnect >= -1
    except:
        _LOGGER.error(
            "IMA Protect Alarm API didn't answer to the request, unable to set up"
        )
        raise ConfigEntryNotReady
    """
    if (bool(testconnect) and 'pk' not in testconnect[0]):
        _LOGGER.error("IMA Protect Alarm API didn't answer to the request, unable to set up")
        raise ConfigEntryNotReady
    """

    _LOGGER.info("Successfully connected to the IMA Protect Alarm API.")

    if config.get(CONF_USERNAME) and config.get(CONF_PASSWORD):
        _LOGGER.debug(
            "Authenticated as %s.",
            config.get(CONF_USERNAME),
        )

    undo_listener = entry.add_update_listener(_async_update_listener)

    hass.data[DOMAIN][entry.entry_id] = {
        CONF_NAME: config.get(CONF_NAME),
        CONTROLLER: controller,
        CONFIG: config,
        UNDO_UPDATE_LISTENER: undo_listener,
    }

    device_registry = await dr.async_get_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, controller.username)},
        manufacturer="IMA",
        model="Protect",
        name=config.get(CONF_NAME),
    )

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    hass.data[DOMAIN][entry.entry_id][UNDO_UPDATE_LISTENER]()

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
