"""StarlingHomeHubEntity class."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .models import SpecificDevice
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

        model = "Unknown"

        if device_properties["type"] == "protect":
            model = "Nest Protect"

        if device_properties["type"] == "cam":
            model = device_properties["cameraModel"]

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_properties["name"],
            model=model,
            manufacturer="Google",
            suggested_area=device_properties["where"],
            serial_number=device_properties["serialNumber"]
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    def get_device(self) -> SpecificDevice:
        """Get the actual device data from coordinator."""
        return self.coordinator.data.devices.get(self.device_id)
