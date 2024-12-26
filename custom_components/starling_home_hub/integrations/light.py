"""Integrations for the light control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# Light specific entities handled by the light entity directly
LIGHT_PLATFORMS = from_base_entities()
