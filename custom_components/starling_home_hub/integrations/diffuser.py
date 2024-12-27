"""Integrations for the diffuser control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# Diffuser specific entities handled by the light entity directly
DIFFUSER_PLATFORMS = from_base_entities()
