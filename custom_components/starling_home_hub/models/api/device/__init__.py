"""Contains all the devices supported by the Starling Home Hub integration."""

from dataclasses import dataclass


@dataclass
class Device[T]:
    """Class that reflects a specific device."""

    status: str
    properties: T


@dataclass
class DeviceUpdate:
    """Class that reflects a specific device update."""

    status: str
    setStatus: dict[str, str]
