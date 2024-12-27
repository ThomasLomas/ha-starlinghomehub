"""Integration for switches."""

from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import Platform

from custom_components.starling_home_hub.entities.switch import StarlingHomeHubSwitchEntityDescription
from custom_components.starling_home_hub.integrations.base import from_base_entities

SWITCH_PLATFORMS = from_base_entities({
    Platform.SWITCH: [
        StarlingHomeHubSwitchEntityDescription(
            key="is_on",
            name="Is On",
            relevant_fn=lambda device: "isOn" in device,
            value_fn=lambda device: device["isOn"],
            update_field="isOn",
            device_class=SwitchDeviceClass.SWITCH
        ),
    ],
})
