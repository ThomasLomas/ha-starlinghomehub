"""Contains home assistant integrations for the Starling Home Hub. These generally align to the different device categories."""

from custom_components.starling_home_hub.integrations.camera import CAMERA_PLATFORMS
from custom_components.starling_home_hub.integrations.diffuser import DIFFUSER_PLATFORMS
from custom_components.starling_home_hub.integrations.fan import FAN_PLATFORMS
from custom_components.starling_home_hub.integrations.garage import GARAGE_PLATFORMS
from custom_components.starling_home_hub.integrations.heater_cooler import HEATER_COOLER_PLATFORMS
from custom_components.starling_home_hub.integrations.home_away_control import HOME_AWAY_CONTROL_PLATFORMS
from custom_components.starling_home_hub.integrations.humidifier_dehumidifier import HUMIDIFIER_DEHUMIDIFIER_PLATFORMS
from custom_components.starling_home_hub.integrations.kettle import KETTLE_PLATFORMS
from custom_components.starling_home_hub.integrations.light import LIGHT_PLATFORMS
from custom_components.starling_home_hub.integrations.lock import LOCK_PLATFORMS
from custom_components.starling_home_hub.integrations.open_close import OPEN_CLOSE_PLATFORMS
from custom_components.starling_home_hub.integrations.outlet import OUTLET_PLATFORMS
from custom_components.starling_home_hub.integrations.purifier import PURIFIER_PLATFORMS
from custom_components.starling_home_hub.integrations.robot import ROBOT_PLATFORMS
from custom_components.starling_home_hub.integrations.sensor import SENSOR_PLATFORMS
from custom_components.starling_home_hub.integrations.smoke_co_detector import SMOKE_CO_DETECTOR_PLATFORMS
from custom_components.starling_home_hub.integrations.switch import SWITCH_PLATFORMS
from custom_components.starling_home_hub.integrations.thermostat import THERMOSTAT_PLATFORMS
from custom_components.starling_home_hub.integrations.valve import VALVE_PLATFORMS

DEVICE_CATEGORIES_TO_PLATFORMS = {
    "cam": CAMERA_PLATFORMS,
    "diffuser": DIFFUSER_PLATFORMS,
    "fan": FAN_PLATFORMS,
    "garage": GARAGE_PLATFORMS,
    "heater_cooler": HEATER_COOLER_PLATFORMS,
    "home_away_control": HOME_AWAY_CONTROL_PLATFORMS,
    "humidifier_dehumidifier": HUMIDIFIER_DEHUMIDIFIER_PLATFORMS,
    "kettle": KETTLE_PLATFORMS,
    "light": LIGHT_PLATFORMS,
    "lock": LOCK_PLATFORMS,
    "open_close": OPEN_CLOSE_PLATFORMS,
    "outlet": OUTLET_PLATFORMS,
    "purifier": PURIFIER_PLATFORMS,
    "robot": ROBOT_PLATFORMS,
    "sensor": SENSOR_PLATFORMS,
    "smoke_co_detector": SMOKE_CO_DETECTOR_PLATFORMS,
    "switch": SWITCH_PLATFORMS,
    "thermostat": THERMOSTAT_PLATFORMS,
    "valve": VALVE_PLATFORMS,
}
