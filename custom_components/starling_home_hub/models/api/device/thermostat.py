"""Class that reflects type=thermostat."""

from dataclasses import dataclass

from custom_components.starling_home_hub.models.api.device.base import BaseDevice


@dataclass
class ThermostatDevice(BaseDevice):
    """Class that reflects type=thermostat."""

    currentTemperature: float
    targetTemperature: float

    targetHeatingThresholdTemperature: float
    targetCoolingThresholdTemperature: float

    hvacMode: str
    hvacState: str

    canHeat: bool
    canCool: bool
    canHeatCool: bool
    canHumidify: bool
    canDehumidify: bool

    fanRunning: bool

    ecoMode: bool

    humidityPercent: float
    targetHumidity: float
    minTargetHumidity: float
    maxTargetHumidity: float

    presetSelected: str
    presetsAvailable: str

    backplateTemperature: float
    sensorSelected: str
    sensorsAvailable: str

    isOnline: bool
