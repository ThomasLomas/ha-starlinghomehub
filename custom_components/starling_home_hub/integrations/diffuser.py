"""Integrations for the diffuser control."""

from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import Platform

from custom_components.starling_home_hub.entities.switch import StarlingHomeHubSwitchEntityDescription
from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo: brightness, hue, saturation
DIFFUSER_PLATFORMS = from_base_entities({
    Platform.SWITCH: [
        StarlingHomeHubSwitchEntityDescription(
            key="is_on",
            name="Is On",
            relevant_fn=lambda device: "isOn" in device,
            value_fn=lambda device: device["isOn"],
            icon="mdi:scent",
            update_field="isOn",
            device_class=SwitchDeviceClass.SWITCH
        ),
    ]
})