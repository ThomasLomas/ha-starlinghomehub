"""Integrations for the lock control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo: currentState, doorSensorState, lastLockUnlockMethod, targetLockState, targetState
LOCK_PLATFORMS = from_base_entities()
