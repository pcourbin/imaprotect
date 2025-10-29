"""Constants for the IMA Protect integration."""
import logging
from datetime import timedelta

from homeassistant.const import STATE_ALARM_ARMED_AWAY
from homeassistant.const import STATE_ALARM_ARMED_HOME
from homeassistant.const import STATE_ALARM_DISARMED

DOMAIN = "imaprotect"

LOGGER = logging.getLogger(__package__)

CONF_ALARM_CODE = "alarm_code"
CONF_SELENIUM_WEBDRIVER = "selenium_webdriver"
CONF_IMA_CONTRACT_NUM = "ima_contract_num"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

ALARM_STATE_TO_HA = {
    0: STATE_ALARM_DISARMED,
    1: STATE_ALARM_ARMED_HOME,
    2: STATE_ALARM_ARMED_AWAY,
}
