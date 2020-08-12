"""Platform for sensor integration."""
import asyncio
import logging
import json

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
    # NOTE example: async_add_entities([MetWeather(config_entry.data, hass.config.units.is_metric)])
    
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    #example_data = {}
    #example_sensor_data = example_data

    arg_x = "arg X value"
    arg_y = "arg Y value"

    async_add_entities(
        [
            ExampleSensor(config_entry, coordinator, "Dazed"),
            TrueNASSensor(config_entry, coordinator, "example_data")
        ]
    ) # something like this ??


class ExampleSensor(Entity):
    """Representation an example temperature sensor."""

    def __init__(self, arg1_config, coordinator, dazed):
        """Initialize the sensor."""

        self.coordinator = coordinator

        self._config = arg1_config
        #self._name = arg1_config.title +' Example'

        self._sensor_data = {}

        self._name = coordinator.data['sensor_name']
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
            'data': self._sensor_data,
            "Count": self._count,
            "Fake": "shit"
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
        
        await self.coordinator.async_request_refresh()

        #self._name = self._sensor_data['data']['sensor_name']
        #self._state = self.hass.data[DOMAIN]['cpu.sensor']['cpu_temp']
        self._count = self.coordinator.data['count']
        self._state = self.coordinator.data['cpu_temp']










class TrueNASSensor(Entity):
    # NOTE: https://github.com/home-assistant/core/blob/dev/homeassistant/components/plaato/sensor.py#L69
    """Representation of the system sensor."""
    def __init__(self, arg1_config, arg_y, confused):
        """Initialize the sensor."""

        self._config = arg1_config
        
        self.coordinator = arg_y
        self._data = confused
        
        self._state = None
        self._connected = False
        self._cpu_temp = 0
        
        ## TODO -- Get this sort in my head -- 
        ## -ONE-:  self._devide_id = arg1_config["device_id"]
        ## -TWO-:  self._devide_id = self._config["device_id"]
        ## Try to use the variable value in a property will error -- CONF_DEVICE_ID is not defined
        ## - See @property "state_attributes" -- NOTE: Set at top of file instead
        #
        #CONF_DEVICE_ID = "device_id"
        #self._devide_id = arg1_config.data[CONF_DEVICE_ID]
        #
        #self._config = arg1_config.data > Results is error > unable to serialize JSON: type mapping error
        #self._devide_id = arg1_config.options[CONF_DEVICE_ID]

        self._name = arg1_config.title + ' Status'
        
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
            "CPU Temp": self._cpu_temp,
            "STATE_ATTR_STATUS": self._state,
            
            #"arg_2 -- value of arg_y": self.arg_2,
            #"arg_3 constant 'confused'": self.arg_3,
            "Value": "another constant value",

            # Helper attr to help me understand
            "config_entry": self._config,

            # -- worked but called twic
            # "coordinator data": self._data(),
            #"coordinator data": self._data,
        }

    @property
    def entity_registry_enabled_default(self):
        """Return if the entity should be enabled when first added to the entity registry."""
        return True

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Brother entity."""
        #await self.coordinator.async_request_refresh()

        # https://developers.home-assistant.io/docs/entity_index#updating-the-entity
        # This is the only method that should fetch new data for Home Assistant.
        """ Fetch new state data for the sensor. """
        # TODO: Something relevant here... sync library or something
        #self._state = self.hass.data[GM_DOMAIN]['state']
        #self._connected = self.hass.data[DOMAIN]['connected']
        #self._state = self.hass.data[DOMAIN][STATE_ATTR_STATUS],
        #self._cpu_temp = self.hass.data[DOMAIN]['cpu_temp']
