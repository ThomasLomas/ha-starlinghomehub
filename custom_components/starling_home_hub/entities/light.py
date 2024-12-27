"""Implements the Starling Home Hub Light entity."""

from typing import Any

from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_COLOR_TEMP_KELVIN, ATTR_HS_COLOR, ColorMode, LightEntity
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util import color

from custom_components.starling_home_hub.const import LOGGER
from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entities import StarlingHomeHubEntity

MIN_HUE = 0
MAX_HUE = 360
MIN_SATURATION = 0
MAX_SATURATION = 100

# Default to the Philips Hue value that HA has always assumed
# https://developers.meethue.com/documentation/core-concepts
# https://developers.home-assistant.io/blog/2024/12/14/kelvin-preferred-color-temperature-unit
DEFAULT_MIN_KELVIN = 2000  # 500 mireds
DEFAULT_MAX_KELVIN = 6535  # 153 mireds


class StarlingHomeHubLightEntity(StarlingHomeHubEntity, LightEntity):
    """Light entity class."""

    def __init__(
        self, device_id: str, coordinator: StarlingHomeHubDataUpdateCoordinator
    ) -> None:
        """Initialize the Light class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self._attr_unique_id = f"{device_id}-light"
        self._attr_min_color_temp_kelvin = DEFAULT_MIN_KELVIN
        self._attr_max_color_temp_kelvin = DEFAULT_MAX_KELVIN
        self._attr_has_entity_name = True

        super().__init__(coordinator)

        device = self.get_device()
        self._attr_name = device.properties["name"]

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        try:
            _on_args = {"isOn": True}

            if ATTR_BRIGHTNESS in kwargs:
                _on_args["brightness"] = round(
                    (kwargs.get(ATTR_BRIGHTNESS) / 255) * 100
                )

            if self.color_mode == ColorMode.HS and ATTR_HS_COLOR in kwargs:
                _on_args["hue"] = kwargs.get(ATTR_HS_COLOR)[0]
                _on_args["saturation"] = kwargs.get(ATTR_HS_COLOR)[1]
            elif (
                self.color_mode == ColorMode.COLOR_TEMP
                and ATTR_COLOR_TEMP_KELVIN in kwargs
            ):
                _on_args["colorTemperature"] = color.color_temperature_kelvin_to_mired(
                    kwargs.get(ATTR_COLOR_TEMP_KELVIN)
                )

            LOGGER.info(
                f"STARLING = {self.get_device().properties["name"]}, color_mode:{
                    self.color_mode}, kwargs:{kwargs}, onargs:{_on_args}"
            )

            await self.coordinator.update_device(
                device_id=self.device_id,
                update=_on_args,
            )
        except Exception as err:
            raise HomeAssistantError(
                f"Error turning {self.entity_id} on {
                    kwargs} with args({_on_args}): {err}"
            ) from err

    async def async_turn_off(self, **kwargs):
        """Turn device off."""
        try:
            await self.coordinator.update_device(
                device_id=self.device_id, update={"isOn": False}
            )
        except Exception as err:
            raise HomeAssistantError(
                f"Error turning {self.entity_id} off {
                    kwargs}: {err}"
            ) from err

    @staticmethod
    def convert_brightness(brightness, target_platform):
        """Convert brightness to the expected values of the target platform (HA = 0-255, Starling = 0-100)."""
        if target_platform == "starling":
            return round((brightness / 255) * 100)
        return round(brightness * 2.55)

    @property
    def available(self) -> bool:
        """Return device availability."""
        return self.get_device() is not None and self.get_device().properties["isOnline"]

    @property
    def is_on(self) -> bool:
        """Return device power on state."""
        return self.get_device().properties["isOn"]

    @property
    def brightness(self) -> int | None:
        """Return the current brightness."""
        device = self.get_device()

        if "brightness" not in device.properties:
            return None

        return self.convert_brightness(device.properties["brightness"], "ha")

    @property
    def color_temp_kelvin(self):
        """Return the color_temp of the light."""
        device = self.get_device()

        if "colorTemperature" not in device.properties:
            return None

        return color.color_temperature_mired_to_kelvin(
            device.properties["colorTemperature"]
        )

    # @property
    # def color_temp(self) -> int | None:
    #     """Return the current color temperature in Kelvin."""
    #     device = self.get_device()
    #     if "colorTemperature" not in device.properties:
    #         return None

    #     return device.properties["colorTemperature"]

    @property
    def hs_color(self) -> tuple[int, int] | None:
        """Return the current hue and saturation."""
        device = self.get_device()

        if "hue" not in device.properties or "saturation" not in device.properties:
            return None

        return [device.properties["hue"], device.properties["saturation"]]

    @property
    def color_mode(self) -> str:
        """Return the current color mode."""
        supported_modes = self.supported_color_modes
        if supported_modes is None:
            return None

        if (
            ColorMode.COLOR_TEMP in supported_modes
            and self.color_temp_kelvin is not None
        ):
            return ColorMode.COLOR_TEMP

        if ColorMode.HS in supported_modes and self.hs_color is not None:
            return ColorMode.HS

        if ColorMode.BRIGHTNESS in supported_modes and self.brightness is not None:
            return ColorMode.BRIGHTNESS

        return ColorMode.ONOFF

    @property
    def supported_color_modes(self) -> set | None:
        """Return the supported color modes."""
        device = self.get_device()

        supported_modes = set()

        if "colorTemperature" in device.properties:
            supported_modes.add(ColorMode.COLOR_TEMP)

        if "hue" in device.properties and "saturation" in device.properties:
            supported_modes.add(ColorMode.HS)

        if "brightness" in device.properties and len(supported_modes) == 0:
            supported_modes.add(ColorMode.BRIGHTNESS)

        if len(supported_modes) == 0:
            supported_modes.add(ColorMode.ONOFF)

        return supported_modes

    async def async_set_color_temp(self, **kwargs: Any) -> None:
        """Set new color temperature."""
        temp = color.color_temperature_kelvin_to_mired(
            kwargs.get(ATTR_COLOR_TEMP_KELVIN)
        )
        LOGGER.info(f"SET COLOR TEMP {temp}")

        try:
            await self.coordinator.update_device(
                device_id=self.device_id, update={"colorTemperature": temp}
            )
        except Exception as err:
            raise HomeAssistantError(
                f"Error setting {self.entity_id} color temperature to {
                    kwargs}: {err}"
            ) from err

    async def async_set_brightness(self, **kwargs: Any) -> None:
        """Set new brightness."""
        brightness = self.convert_brightness(
            kwargs.get(ATTR_BRIGHTNESS), "starling")
        LOGGER.info(f"SET BRIGHTNESS {brightness}")

        try:
            await self.coordinator.update_device(
                device_id=self.device_id, update={"brightness": brightness}
            )
        except Exception as err:
            raise HomeAssistantError(
                f"Error setting {self.entity_id} brightness to {
                    kwargs}: {err}"
            ) from err

    async def async_set_hs_color(self, **kwargs: Any) -> None:
        """Set new color via hue and saturation."""
        hue = kwargs.get(ATTR_HS_COLOR)[0]
        saturation = kwargs.get(ATTR_HS_COLOR)[1]
        LOGGER.info(f"SET HS COLOR {hue} {saturation}")

        try:
            if (
                MIN_HUE <= hue <= MAX_HUE
                and MIN_SATURATION <= saturation <= MAX_SATURATION
            ):
                await self.coordinator.update_device(
                    device_id=self.device_id,
                    update={"hue": hue, "saturation": saturation},
                )
            else:
                raise Exception(
                    "Hue and Saturation are outside of the acceptable range: "
                    + f"Hue({MIN_HUE},{MAX_HUE}), Saturation({MIN_SATURATION, MAX_SATURATION})"
                )
        except Exception as err:
            raise HomeAssistantError(
                f"Error setting {self.entity_id} hs_color to {
                    kwargs}: {err}"
            ) from err
