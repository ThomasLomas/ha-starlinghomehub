"""This module contains the CoordinatorData class."""
from dataclasses import dataclass

from custom_components.starling_home_hub.models.api.device import Device
from custom_components.starling_home_hub.models.api.status import Status


@dataclass
class CoordinatorData:
    """Class that houses all the coordinator data required."""

    devices: dict[str, Device]
    status: Status
