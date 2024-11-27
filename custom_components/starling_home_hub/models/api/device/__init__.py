""" Contains all the devices supported by the Starling Home Hub integration. """

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass
class Device(Generic[T]):
    """Class that reflects a specific device."""

    status: str
    properties: T
