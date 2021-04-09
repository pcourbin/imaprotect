"""Support for the IMA Protect Alarm."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from .const import (
    CONFIG,
    CONTROLLER,
    DOMAIN,
    MIN_TIME_BETWEEN_UPDATES,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default="IMA Protect Alarm"): str,
        vol.Optional(CONF_USERNAME): str,
        vol.Optional(CONF_PASSWORD): str,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Import the platform into a config entry."""

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=config
        )
    )


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the IMA Protect Alarm platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    controller = data[CONTROLLER]
    controller_name = data[CONF_NAME]
    #config = data[CONFIG]

    entities = []

    _LOGGER.debug("Add the Alarm Status entity.")
    entities.append(
        IMAProtectAlarm(
            controller,
            controller_name,
            "Alarm Status"
        )
    )

    if entities:
        async_add_entities(entities, True)


class IMAProtectAlarm(Entity):
    """Representation of a Sensor."""

    def __init__(self, controller, controller_name, name):
        """Initialize the sensor."""
        self._controller = controller
        self._controller_name = controller_name
        self._name = controller_name+" -- "+name
        self._device_class = None

        self._state = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._controller.username)},
            "name": self._controller_name,
            "manufacturer": "IMA",
            "model": "Protect",
            "via_device": (DOMAIN, self._controller.username),
        }

    @property
    def unique_id(self):
        return f"imaprotect{self._controller_name}_{self._name}_status"

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        icon = 'mdi:home-lock'
        if (self._state == 0):
            icon = 'mdi:home-lock-open'
        return icon

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self._state = self._controller.get_status() + 1
