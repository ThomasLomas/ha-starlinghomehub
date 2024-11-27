"""This module contains the Devices class."""
from dataclasses import dataclass

from custom_components.starling_home_hub.models.api.device.base import BaseDevice


@dataclass
class Devices:
    """Class that reflects a devices response."""

    status: bool
    devices: list[BaseDevice]
