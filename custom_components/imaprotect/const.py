"""Constants for the IMA Protect integration."""
import logging
from datetime import timedelta

from homeassistant.components.alarm_control_panel import AlarmControlPanelState

DOMAIN = "imaprotect"

LOGGER = logging.getLogger(__package__)

CONF_ALARM_CODE = "alarm_code"
CONF_SELENIUM_WEBDRIVER = "selenium_webdriver"
CONF_IMA_CONTRACT_NUM = "ima_contract_num"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

ALARM_STATE_TO_HA = {
    0: AlarmControlPanelState.DISARMED,
    1: AlarmControlPanelState.ARMED_HOME,
    2: AlarmControlPanelState.ARMED_AWAY,
}
