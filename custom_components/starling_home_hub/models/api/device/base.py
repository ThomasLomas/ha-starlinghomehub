"""This contains the base device class."""

from dataclasses import dataclass


@dataclass
class BaseDevice:
    """Class that reflects a device."""

    type: str
    category: str
    id: str
    name: str
    model: str
    roomId: str
    roomName: str
    structureId: str
    structureName: str
    serialNumber: str
