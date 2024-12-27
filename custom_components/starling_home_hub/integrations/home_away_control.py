"""Integrations for the Home away control."""

from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import Platform

from custom_components.starling_home_hub.entities.switch import StarlingHomeHubSwitchEntityDescription

HOME_AWAY_CONTROL_PLATFORMS = {
    Platform.SWITCH: [
        StarlingHomeHubSwitchEntityDescription(
            key="home_state",
            name="Home Occupied",
            relevant_fn=lambda device: "homeState" in device,
            value_fn=lambda device: device["homeState"],
            icon="mdi:home",
            update_field="homeState",
            device_class=SwitchDeviceClass.SWITCH
        ),
    ]
}
