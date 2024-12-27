"""Integrations for the kettle control."""

from custom_components.starling_home_hub.integrations.base import from_base_entities

# todo: targetTemperature
KETTLE_PLATFORMS = from_base_entities({
    # Platform.SWITCH: [
    #     StarlingHomeHubSwitchEntityDescription(
    #         key="is_on",
    #         name="Is On",
    #         relevant_fn=lambda device: "isOn" in device,
    #         value_fn=lambda device: device["isOn"],
    #         update_field="isOn",
    #         device_class=SwitchDeviceClass.SWITCH
    #     ),
    # ],
    # Platform.BINARY_SENSOR: [
    # StarlingHomeHubBinarySensorEntityDescription(
    #     key="can_heat",
    #     name="Can Heat",
    #     value_fn=lambda device: device["canHeat"],
    #     relevant_fn=lambda device: "canHeat" in device,
    #     device_class=BinarySensorDeviceClass.HEAT,
    #     entity_category=EntityCategory.DIAGNOSTIC,
    # ),
    # StarlingHomeHubBinarySensorEntityDescription(
    #     key="state",
    #     name="Heating",
    #     value_fn=lambda device: device["state"] == "heating",
    #     relevant_fn=lambda device: "state" in device,
    #     device_class=BinarySensorDeviceClass.HEAT,
    # ),
    # ],
    # Platform.SENSOR: [
    # StarlingHomeHubSensorEntityDescription(
    #     key="current_temperature",
    #     name="Current Temperature",
    #     relevant_fn=lambda device: "currentTemperature" in device,
    #     value_fn=lambda device: device["currentTemperature"],
    #     native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # ]
})
