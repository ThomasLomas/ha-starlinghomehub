"""Contains home assistant integrations for the Starling Home Hub. These generally align to the different device categories."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.helpers.typing import StateType

D = TypeVar("D")


@dataclass
class StarlingHomeHubSensorEntityDescription(SensorEntityDescription):
    """Class to describe a home hub sensor."""

    value_fn: Callable[[D], StateType] | None = None
    relevant_fn: Callable[[D], StateType] | None = None


@dataclass
class StarlingHomeHubBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class to describe a home hub binary sensor."""

    value_fn: Callable[[D], StateType] | None = None
    relevant_fn: Callable[[D], StateType] | None = None


@dataclass
class StarlingHomeHubSwitchEntityDescription(SwitchEntityDescription):
    """Class to describe a home hub switch."""

    value_fn: Callable[[D], StateType] | None = None
    relevant_fn: Callable[[D], StateType] | None = None
    update_field: str | None = None


@dataclass
class StarlingHomeHubSelectEntityDescription(SelectEntityDescription):
    """Class to describe a home hub select."""

    value_fn: Callable[[D], StateType] | None = None
    relevant_fn: Callable[[D], StateType] | None = None
    update_field: str | None = None
    icon_fn: Callable[[D], str] | None = None
