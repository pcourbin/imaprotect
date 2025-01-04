"""Support for IMA Protect devices."""
from __future__ import annotations

import homeassistant.helpers.config_validation as cv
from homeassistant.components.alarm_control_panel import (
    DOMAIN as ALARM_CONTROL_PANEL_DOMAIN,
)
from homeassistant.components.camera import (
    DOMAIN as CAMERA_DOMAIN,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN
from .coordinator import IMAProtectDataUpdateCoordinator

PLATFORMS = [
    ALARM_CONTROL_PANEL_DOMAIN,
    CAMERA_DOMAIN,
]

CONFIG_SCHEMA = cv.deprecated(DOMAIN)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up IMA Protect from a config entry."""
    coordinator = IMAProtectDataUpdateCoordinator(hass, entry=entry)

    if not await coordinator.async_login():
        raise ConfigEntryAuthFailed

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, coordinator.async_logout)
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up all platforms for this device/entry.
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload IMA Protect config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False

    del hass.data[DOMAIN][entry.entry_id]

    if not hass.data[DOMAIN]:
        del hass.data[DOMAIN]

    return True
