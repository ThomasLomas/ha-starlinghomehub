"""Class that reflects type=smoke_detector."""

from dataclasses import dataclass

from custom_components.starling_home_hub.models.api.device.base import BaseDevice


@dataclass
class SmokeDetectorDevice(BaseDevice):
    """Class that reflects type=smoke_detector."""

    smokeDetected: bool
    coDetected: bool
    batteryStatus: str
    batteryLevel: int
    manualTestActive: bool
    smokeStateDetail: str
    coLevel: int
    alarmSilenced: bool
