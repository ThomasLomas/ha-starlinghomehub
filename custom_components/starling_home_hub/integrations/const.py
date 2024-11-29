from custom_components.starling_home_hub.integrations.camera import CAMERA_PLATFORMS
from custom_components.starling_home_hub.integrations.sensor import SENSOR_PLATFORMS
from custom_components.starling_home_hub.integrations.smoke_detector import SMOKE_DETECTOR_PLATFORMS

# "cam", "diffuser", "fan", "garage", "heater_cooler", "humidifer_dehumidifier", "kettle", "light", "lock", "open_close", "outlet", "purifier", "robot", "sensor", "smoke_co_detector", "switch", "thermostat", "valve"
DEVICE_CATEGORIES_TO_PLATFORMS = {
    "cam": CAMERA_PLATFORMS,
    "smoke_co_detector": SMOKE_DETECTOR_PLATFORMS,
    "sensor": SENSOR_PLATFORMS,
}
