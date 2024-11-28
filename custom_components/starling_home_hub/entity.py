"""Starling Home Hub entities and their descriptions."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.models.api.device import Device

from .const import ATTRIBUTION, DOMAIN
from .coordinator import StarlingHomeHubDataUpdateCoordinator


class StarlingHomeHubEntity(CoordinatorEntity):
    """StarlingHomeHubEntity class."""

    device_id: str

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: StarlingHomeHubDataUpdateCoordinator) -> None:
        """Initialize."""

        super().__init__(coordinator)

        device = self.get_device()
        device_properties = device.properties
        device_id = device_properties["id"]
        model = device_properties["model"]

        manufacturer = "Unknown"
        if model.startswith("Nest"):
            manufacturer = "Google"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_properties["name"],
            model=model,
            manufacturer=manufacturer,
            suggested_area=device_properties["roomName"],
            serial_number=device_properties["serialNumber"]
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    def get_device(self) -> Device:
        """Get the actual device data from coordinator."""
        return self.coordinator.data.devices.get(self.device_id)


class StarlingHomeHubSensorEntity(StarlingHomeHubEntity, SensorEntity):
    """Starling Home Hub Sensor Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the Sensor Entity class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        super().__init__(coordinator)

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)


class StarlingHomeHubBinarySensorEntity(StarlingHomeHubEntity, BinarySensorEntity):
    """Starling Home Hub Binary Sensor Entity class."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the Binary Sensor class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self.entity_description = entity_description
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        super().__init__(coordinator)

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.get_device().properties)
