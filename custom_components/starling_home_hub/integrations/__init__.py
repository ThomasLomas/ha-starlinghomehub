"""Contains home assistant integrations for the Starling Home Hub. These generally align to the different device categories."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.helpers.typing import StateType

D = TypeVar("D")


@dataclass
class StarlingHomeHubSensorDescription(SensorEntityDescription):
    """Class to describe a home hub sensor."""

    value_fn: Callable[[D], StateType] | None = None
    relevant_fn: Callable[[D], StateType] | None = None


@dataclass
class StarlingHomeHubBinarySensorDescription(BinarySensorEntityDescription):
    """Class to describe a home hub binary sensor."""

    value_fn: Callable[[D], StateType] | None = None
    relevant_fn: Callable[[D], StateType] | None = None
