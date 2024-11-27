"""Class that reflects type=camera."""

from dataclasses import dataclass

from custom_components.starling_home_hub.models.api.device.base import BaseDevice


@dataclass
class CameraDevice(BaseDevice):
    """Class that reflects type=camera."""

    supportsStreaming: bool
