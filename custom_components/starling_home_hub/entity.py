"""StarlingHomeHubEntity class."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
