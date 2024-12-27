"""Integration for valves."""

from homeassistant.components.valve import ValveDeviceClass
from homeassistant.const import Platform

from custom_components.starling_home_hub.entities.valve import StarlingHomeHubValveEntityDescription
from custom_components.starling_home_hub.integrations.base import from_base_entities

VALVE_PLATFORMS = from_base_entities({
    Platform.VALVE: [
        StarlingHomeHubValveEntityDescription(
            key="is_on",
            name="Is On",
            relevant_fn=lambda device: "isOn" in device,
            value_fn=lambda device: device["isOn"],
            update_field="isOn",
            device_class=ValveDeviceClass.WATER,
        ),
    ],
})
