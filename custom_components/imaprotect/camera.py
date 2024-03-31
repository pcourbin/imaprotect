"""Support for IMA Protect alarm control panels."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Callable

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ALARM_STATE_TO_HA
from .const import DOMAIN
from .coordinator import IMAProtectDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[Iterable[Entity]], None],
) -> None:
    """Set up IMA Protect alarm control panel from a config entry."""
    cams: list[IMAProtectCamera] = []
    for cn, cv in hass.data[DOMAIN][entry.entry_id].data["cameras"].items():
        cams.append(
            IMAProtectCamera(
                hass=hass, name=cn, coordinator=hass.data[DOMAIN][entry.entry_id]
            )
        )
    async_add_entities(cams)


class IMAProtectCamera(CoordinatorEntity, Camera):
    """Representation of an IMAProtect camera feed."""

    coordinator: IMAProtectDataUpdateCoordinator

    _attr_has_entity_name = True

    _state: str | None = None
    _armed_away: bool = False

    _hass: HomeAssistant

    _pic: bytes | None = None
    _pic_url: str | None = None
    _pic_outdated: bool = True

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        coordinator: IMAProtectDataUpdateCoordinator,
    ) -> None:
        """Initialize the camera object."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._hass = hass
        self._state = None
        self._armed_away = False
        self._pic = None
        self._attr_name = name

    @property
    def motion_detection_enabled(self) -> bool:
        return self._armed_away

    @property
    def is_on(self) -> bool:
        return self._armed_away

    @property
    def brand(self):
        return "IMA Protect"

    @property
    def supported_features(self) -> int:
        """We can't be powered on/off, and we can't stream. Woops"""
        return 0

    @callback
    def _handle_coordinator_update(self) -> None:
        self._armed_away = ALARM_STATE_TO_HA.get(self.coordinator.data["alarm"] == 2)
        mycam = self.coordinator.data["cameras"][self._attr_name]
        if len(mycam) == 0:
            self._pic_url = None
        elif self._pic_url != mycam[0]["images"][0]:
            self._pic_url = "https://www.imaprotect.com" + mycam[0]["images"][0]
            self._pic_outdated = True
        super()._handle_coordinator_update()

    async def async_camera_image(self, width=None, height=None) -> bytes | None:
        if self._pic_url is None:
            return None
        elif self._pic_outdated:
            picrq = await self._hass.async_add_executor_job(
                self.coordinator.imaprotect._session.get, self._pic_url
            )
            self._pic = picrq.content
            self._pic_outdated = False
        return self._pic
