"""Platform for sensor integration."""

import asyncio
import logging

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
    STATE_ATTR_STATUS,
    STATE_ATTR_VERSION,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add a weather entity from a config_entry."""
    
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Example: async_add_entities([MetWeather(config_entry.data, hass.config.units.is_metric)])
    async_add_entities(
        [
            ExampleSensor(config_entry, coordinator, "Confused"),
            TrueNASSensor(config_entry, coordinator)
        ]
    ) # ---- ^ This seems to work OK ^


class ExampleSensor(Entity):
    """Representation an example temperature sensor."""

    def __init__(self, arg1_config, coordinator, dazed):
        """Initialize the sensor."""
        #self._name = arg1_config.title +' Example'
        self._config = arg1_config
        self.coordinator = coordinator
        self._name = coordinator.data['sensor_name']

        self._dazed = dazed
        self._state = 0
        self._count = 0
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def unique_id(self):
        return self._config.entry_id + '-cpu'

    @property
    def state_attributes(self):
        """Return the state attributes of the sun."""
        return {
            "count": self._count,
            "dazed": self._dazed,
            # see it, helps here me understand
            "config_entry": self._config, 
        }

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def entity_registry_enabled_default(self):
        """Return if the entity should be enabled when first added to the entity registry."""
        return True

    async def async_update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("update sensor 1")
        #await self.coordinator.async_request_refresh()
        self._count = self.coordinator.data['count']
        self._state = self.coordinator.data['cpu_temp']



class TrueNASSensor(Entity):
    """Representation of a system information sensor."""
    def __init__(self, config_entry, coordinator):
        """Initialize the sensor."""

        self.coordinator = coordinator
        self._info = coordinator.data['system_info']
        self._config = config_entry
        #self._name = config_entry.title + coordinator.data['sensor_name']
        self._name = config_entry.title + ' status'
 
        self._state = None
        self._info = None
        self._version = None
        self._uptime = None
                
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def unique_id(self):
        return self._config.entry_id + '-status'

    @property
    def state_attributes(self):
        """Return the state attributes of the sun."""
        return {
            "Title": self._config.title,
            "Version": self._version,
            "Uptime": self._uptime,
            "Info": self._info,
        }

    @property
    def entity_registry_enabled_default(self):
        """Return if the entity should be enabled when first added to the entity registry."""
        return True

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success
    
    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications.
        NOTE Only add this once. Get updated based on scan interval (see __init__.py)
        """
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Fetch new state data for the sensor."""
        #await self.coordinator.async_request_refresh()
        _LOGGER.debug("update sensor 2")
        self._state = self.coordinator.data['system_state']
        self._info = self.coordinator.data['system_info']
        self._version = self.coordinator.data['system_info']['version']
        self._uptime = self.coordinator.data['system_info']['uptime']
