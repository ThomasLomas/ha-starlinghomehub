"""Light integration for Starling Home Hub."""

import math
from functools import cached_property
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.light import (ATTR_BRIGHTNESS, ATTR_COLOR_TEMP_KELVIN, ATTR_HS_COLOR, ATTR_RGB_COLOR, ATTR_RGBW_COLOR,
                                            ATTR_XY_COLOR, ColorMode, LightEntity)
from homeassistant.const import Platform
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util.color import value_to_brightness, brightness_to_value

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entity import StarlingHomeHubEntity
from custom_components.starling_home_hub.integrations import ALL_ENTITY_DESCRIPTIONS_TYPES, StarlingHomeHubBinarySensorEntityDescription

LIGHT_PLATFORMS: dict[Platform, list[ALL_ENTITY_DESCRIPTIONS_TYPES]] = {
    Platform.BINARY_SENSOR: [
        StarlingHomeHubBinarySensorEntityDescription(
            key="is_online",
            name="Is Online",
            relevant_fn=lambda device: "isOnline" in device,
            value_fn=lambda device: device["isOnline"],
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ],
}

BRIGHTNESS_SCALE = (1, 100)


class StarlingHomeHubLightEntity(StarlingHomeHubEntity, LightEntity):
    """Starling Home Hub Light Entity."""

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator,
    ) -> None:
        """Initialize the Switch class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self._attr_unique_id = f"{device_id}-light"

        super().__init__(coordinator)
        device = self.get_device()

        self._attr_name = device.properties["name"]
        self._attr_color_mode = next(iter(self.supported_color_modes))

    @cached_property
    def supported_color_modes(self) -> set[ColorMode]:
        """Get supported color modes."""
        color_mode = set()
        device = self.get_device()

        if "colorTemperature" in device.properties:
            color_mode.add(ColorMode.COLOR_TEMP)
        if "hue" in device.properties and "saturation" in device.properties and "brightness" in device.properties:
            color_mode.add(ColorMode.HS)
        if not color_mode:
            if "brightness" in device.properties:
                color_mode.add(ColorMode.BRIGHTNESS)
            else:
                color_mode.add(ColorMode.ONOFF)

        return color_mode

    @property
    def is_on(self) -> bool:
        """Return the state of the light."""
        return self.get_device().properties["isOn"]

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        device = self.get_device()
        if "brightness" in device.properties:
            return value_to_brightness(BRIGHTNESS_SCALE, device.properties["brightness"])
        else:
            return None

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation color value [float, float]."""
        # Hue is scaled 0..360 int encoded in 1 byte in KNX (-> only 256 possible values)
        # Saturation is scaled 0..100 int
        device = self.get_device()

        if "hue" in device.properties and "saturation" in device.properties:
            return (device.properties["hue"], device.properties["saturation"])
        else:
            return None

    @property
    def color_temp(self) -> int:
        """Return the CT color value in mireds."""
        device = self.get_device()
        if "colorTemperature" in device.properties:
            return device.properties["colorTemperature"]
        else:
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        LOGGER.debug(f"Turning on light {self.device_id} with kwargs {kwargs}")

        brightness = kwargs.get(ATTR_BRIGHTNESS)
        # LightEntity color translation will ensure that only attributes of supported
        # color modes are passed to this method - so we can't set unsupported mode here
        if color_temp := kwargs.get(ATTR_COLOR_TEMP_KELVIN):
            self._attr_color_mode = ColorMode.COLOR_TEMP
        if kwargs.get(ATTR_RGB_COLOR):
            self._attr_color_mode = ColorMode.RGB
        if kwargs.get(ATTR_RGBW_COLOR):
            self._attr_color_mode = ColorMode.RGBW
        if hs_color := kwargs.get(ATTR_HS_COLOR):
            self._attr_color_mode = ColorMode.HS
        if kwargs.get(ATTR_XY_COLOR):
            self._attr_color_mode = ColorMode.XY

        update_params = {"isOn": True}

        if brightness is not None:
            update_params["brightness"] = math.ceil(
                brightness_to_value(BRIGHTNESS_SCALE, brightness))

        if hs_color is not None:
            update_params["hue"] = hs_color[0]
            update_params["saturation"] = hs_color[1]

        if color_temp is not None:
            update_params["colorTemperature"] = color_temp

        await self.coordinator.update_device(
            device_id=self.device_id,
            update=update_params
        )

        # todo support color temp

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self.coordinator.update_device(
            device_id=self.device_id,
            update={"isOn": False}
        )
