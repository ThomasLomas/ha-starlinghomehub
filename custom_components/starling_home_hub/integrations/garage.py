"""Garage Platform."""

from homeassistant.components.cover import CoverDeviceClass
from homeassistant.const import Platform

from custom_components.starling_home_hub.entities.cover import StarlingHomeHubCoverEntityDescription
from custom_components.starling_home_hub.integrations.base import from_base_entities

GARAGE_PLATFORMS = from_base_entities({
    Platform.COVER: [
        StarlingHomeHubCoverEntityDescription(
            key="garage_door",
            name="Garage Door",
            relevant_fn=lambda device: "currentState" in device and "targetState" in device,
            current_state_field="currentState",
            target_state_field="targetState",
            device_class=CoverDeviceClass.GARAGE
        ),
    ]
})
