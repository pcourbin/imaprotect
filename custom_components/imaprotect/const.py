"""Constants for the EcoDevices component."""
from datetime import timedelta

DOMAIN = "imaprotect"

CONTROLLER = "controller"
CONFIG = "config"
PLATFORMS = ["sensor"]
UNDO_UPDATE_LISTENER = "undo_update_listener"
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)