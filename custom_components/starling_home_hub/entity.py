"""StarlingHomeHubEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .models import SpecificDevice
from .coordinator import StarlingHomeHubDataUpdateCoordinator

class StarlingHomeHubEntity(CoordinatorEntity):
    """StarlingHomeHubEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: StarlingHomeHubDataUpdateCoordinator, device: SpecificDevice, entity_description: EntityDescription) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.entity_description = entity_description

        device_properties = device.properties
        device_id = device_properties["id"]
        self._attr_unique_id = f"{device_id}-{self.entity_description.key}"

        model = "Unknown"

        if device_properties["type"] == "protect":
            model = "Nest Protect"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_properties["name"],
            model=model,
            manufacturer="Google",
            suggested_area=device_properties["where"]
        )
