"""Tessie binary sensors."""

from homeassistant.components.number import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import callback
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from . import TessieEntity
from homeassistant.const import TEMP_CELSIUS


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup Tessie number entities."""

    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    tessie = data["tessie"]

    entities = []

    for vin, vehicle in coordinator.data.items():
        entities.append(InsideTemperatureSensor(coordinator, vin, tessie))

    async_add_entities(entities)


class InsideTemperatureSensor(TessieEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Vehicle temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.vin}_inside_temperature"

    @property
    def native_value(self) -> float | None:
        """Return charge limit."""

        return self.coordinator.data[self.vin].climate_state.inside_temp
