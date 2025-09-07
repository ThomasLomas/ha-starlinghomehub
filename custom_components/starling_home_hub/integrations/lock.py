"""Integrations for the lock control."""

from homeassistant.const import Platform
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from custom_components.starling_home_hub.entities.binary_sensor import StarlingHomeHubBinarySensorEntityDescription
from custom_components.starling_home_hub.entities.lock import StarlingHomeHubLockEntityDescription
from custom_components.starling_home_hub.integrations.base import from_base_entities


# todo: lastLockUnlockMethod, targetLockState
LOCK_PLATFORMS = from_base_entities({
    Platform.LOCK: [
        StarlingHomeHubLockEntityDescription(
            key="lock",
            name="Lock",
            relevant_fn=lambda device: "currentState" in device and "targetState" in device,
            current_state_field="currentState",
            target_state_field="targetState",
            icon_fn=lambda device: "mdi:lock-open" if device.get(
                "currentState") == "unlocked" else "mdi:lock"
        ),
    ],
    Platform.BINARY_SENSOR: [
        StarlingHomeHubBinarySensorEntityDescription(
            key="door_sensor",
            name="Door Sensor",
            value_fn=lambda device: device["doorSensorState"] == "open",
            relevant_fn=lambda device: "doorSensorState" in device,
            device_class=BinarySensorDeviceClass.DOOR,
        ),
    ],
})
