"""This module implements the Starling Home Hub Thermostat entity."""

from typing import Any

from homeassistant.components.climate import (ATTR_HVAC_MODE, ATTR_TARGET_TEMP_HIGH, ATTR_TARGET_TEMP_LOW, FAN_OFF, FAN_ON, ClimateEntity,
                                              ClimateEntityFeature, HVACAction, HVACMode)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import ATTR_TEMPERATURE, PERCENTAGE, Platform, UnitOfTemperature
from homeassistant.exceptions import HomeAssistantError

from custom_components.starling_home_hub.coordinator import StarlingHomeHubDataUpdateCoordinator
from custom_components.starling_home_hub.entity import StarlingHomeHubEntity
from custom_components.starling_home_hub.integrations import StarlingHomeHubSelectEntityDescription, StarlingHomeHubSensorEntityDescription

MIN_TEMP = 10
MAX_TEMP = 32
MIN_TEMP_RANGE = 1.66667

# Mapping for sdm.devices.traits.ThermostatMode mode field
THERMOSTAT_MODE_MAP: dict[str, HVACMode] = {
    "off": HVACMode.OFF,
    "heat": HVACMode.HEAT,
    "cool": HVACMode.COOL,
    "heatCool": HVACMode.HEAT_COOL,
}
THERMOSTAT_INV_MODE_MAP = {v: k for k, v in THERMOSTAT_MODE_MAP.items()}

THERMOSTAT_PLATFORMS = {
    Platform.SENSOR: [
        StarlingHomeHubSensorEntityDescription(
            key="humidity_percent",
            name="Humidity Percentage",
            relevant_fn=lambda device: "humidityPercent" in device,
            value_fn=lambda device: device["humidityPercent"],
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        StarlingHomeHubSensorEntityDescription(
            key="backplate_temperature",
            name="Blackplate Temperature",
            relevant_fn=lambda device: "backplateTemperature" in device,
            value_fn=lambda device: device["backplateTemperature"],
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ],
    Platform.SELECT: [
        StarlingHomeHubSelectEntityDescription(
            key="display_temperature_units",
            name="Display Temperature Units",
            relevant_fn=lambda device: "displayTemperatureUnits" in device,
            value_fn=lambda device: device["displayTemperatureUnits"],
            icon_fn=lambda device: "mdi:temperature-celsius" if device[
                "displayTemperatureUnits"] == "C" else "mdi:temperature-fahrenheit",
            options=["C", "F"],
            update_field="displayTemperatureUnits",
        )
    ],
}


class StarlingHomeHubThermostatEntity(StarlingHomeHubEntity, ClimateEntity):
    """Thermostat class."""

    _attr_min_temp = MIN_TEMP
    _attr_max_temp = MAX_TEMP
    _attr_has_entity_name = True

    def __init__(
        self,
        device_id: str,
        coordinator: StarlingHomeHubDataUpdateCoordinator
    ) -> None:
        """Initialize the Thermostat class."""

        self.device_id = device_id
        self.coordinator = coordinator
        self._attr_unique_id = f"{device_id}-thermostat"
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_supported_features = self._get_supported_features()
        self._attr_name = "Thermostat"

        device = self.get_device()

        self._attr_hvac_modes = []
        if device.properties["canHeat"]:
            self._attr_hvac_modes.append(HVACMode.HEAT)

        if device.properties["canCool"]:
            self._attr_hvac_modes.append(HVACMode.COOL)

        if device.properties["canHeatCool"]:
            self._attr_hvac_modes.append(HVACMode.HEAT_COOL)

        if len(self._attr_hvac_modes) > 0:
            self._attr_hvac_modes.append(HVACMode.OFF)

        super().__init__(coordinator)

    @property
    def available(self) -> bool:
        """Return device availability."""
        device = self.get_device()
        return device != None and device.properties["isOnline"]

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        device = self.get_device()
        if "currentTemperature" not in device.properties:
            return None

        return device.properties["currentTemperature"]

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature currently set to be reached."""
        device = self.get_device()

        if "targetTemperature" in device.properties and self.hvac_mode == HVACMode.HEAT or self.hvac_mode == HVACMode.COOL:
            return device.properties["targetTemperature"]

        return None

    @property
    def target_temperature_high(self) -> float | None:
        """Return the upper bound target temperature."""
        if self.hvac_mode != HVACMode.HEAT_COOL:
            return None

        device = self.get_device()

        if "targetCoolingThresholdTemperature" in device.properties:
            return device.properties["targetCoolingThresholdTemperature"]

        return None

    @property
    def target_temperature_low(self) -> float | None:
        """Return the lower bound target temperature."""
        if self.hvac_mode != HVACMode.HEAT_COOL:
            return None

        device = self.get_device()

        if "targetHeatingThresholdTemperature" in device.properties:
            return device.properties["targetHeatingThresholdTemperature"]

        return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current operation (e.g. heat, cool, idle)."""
        hvacMode = self.get_device().properties["hvacMode"]

        if hvacMode == "heat":
            return HVACMode.HEAT
        elif hvacMode == "cool":
            return HVACMode.COOL
        elif hvacMode == "heatCool":
            return HVACMode.HEAT_COOL
        else:
            return HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action (heating, cooling)."""
        hvacState = self.get_device().properties["hvacState"]

        if hvacState == "off" and self.hvac_mode != HVACMode.OFF:
            return HVACAction.IDLE

        if hvacState == "heating":
            return HVACAction.HEATING
        elif hvacState == "cooling":
            return HVACAction.COOLING
        elif hvacState == "off":
            return HVACAction.OFF
        else:
            return None

    def _get_supported_features(self) -> ClimateEntityFeature:
        """Compute the bitmap of supported features from the current state."""
        features = ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.TURN_ON

        device = self.get_device()

        if device.properties["canHeatCool"]:
            features |= ClimateEntityFeature.TARGET_TEMPERATURE_RANGE

        if device.properties["canHeat"] or device.properties["canCool"]:
            features |= ClimateEntityFeature.TARGET_TEMPERATURE

        # todo: preset support
        # if "presetsAvailable" in device.properties:
        #     features |= ClimateEntityFeature.PRESET_MODE

        # todo: fan support
        # if "fanRunning" in device.properties:
        #     features |= ClimateEntityFeature.FAN_MODE

        return features

    @property
    def fan_modes(self) -> list[str]:
        """Return the list of available fan modes."""
        if (self.supported_features & ClimateEntityFeature.FAN_MODE):
            return [FAN_ON, FAN_OFF]

        return []

    @property
    def fan_mode(self) -> str:
        """Return the current fan mode."""
        if (self.supported_features & ClimateEntityFeature.FAN_MODE) and self.get_device().properties["fanRunning"]:
            return FAN_ON

        return FAN_OFF

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""

        hvac_mode = self.hvac_mode
        if kwargs.get(ATTR_HVAC_MODE) is not None:
            hvac_mode = kwargs[ATTR_HVAC_MODE]
            await self.async_set_hvac_mode(hvac_mode)

        low_temp = kwargs.get(ATTR_TARGET_TEMP_LOW)
        high_temp = kwargs.get(ATTR_TARGET_TEMP_HIGH)
        temp = kwargs.get(ATTR_TEMPERATURE)

        try:
            if hvac_mode == HVACMode.HEAT_COOL:
                if low_temp and high_temp:
                    if high_temp - low_temp < MIN_TEMP_RANGE:
                        # Ensure there is a minimum gap from the new temp. Pick
                        # the temp that is not changing as the one to move.
                        if abs(high_temp - self.target_temperature_high) < 0.01:
                            high_temp = low_temp + MIN_TEMP_RANGE
                        else:
                            low_temp = high_temp - MIN_TEMP_RANGE

                    await self.coordinator.update_device(
                        device_id=self.device_id,
                        update={"targetCoolingThresholdTemperature": high_temp,
                                "targetHeatingThresholdTemperature": low_temp}
                    )
            elif (hvac_mode == HVACMode.HEAT or hvac_mode == HVACMode.COOL) and temp:
                await self.coordinator.update_device(
                    device_id=self.device_id,
                    update={"targetTemperature": temp}
                )

            await self.coordinator.refresh_data()
        except Exception as err:
            raise HomeAssistantError(
                f"Error setting {self.entity_id} temperature to {
                    kwargs}: {err}"
            ) from err

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode not in self.hvac_modes:
            raise ValueError(f"Unsupported hvac_mode '{hvac_mode}'")

        api_mode = THERMOSTAT_INV_MODE_MAP[hvac_mode]

        try:
            await self.coordinator.update_device(
                device_id=self.device_id,
                update={"hvacMode": api_mode}
            )

            await self.coordinator.refresh_data()
        except Exception as err:
            raise HomeAssistantError(
                f"Error setting {self.entity_id} HVAC mode to {
                    hvac_mode}: {err}"
            ) from err
