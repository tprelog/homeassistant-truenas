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
    # NOTE example: async_add_entities([MetWeather(config_entry.data, hass.config.units.is_metric)])
    
    arg_n = "arg_n value"
    #async_add_entities([TrueNASMusicSensor(config_entry, arg_n, "Blah")]) # maybe Hint hass.config.somethnig??
    async_add_entities([ExampleSensor1(), TrueNASSensor(config_entry, arg_n, "Blah")]) # maybe Hint hass.config.somethnig??


class ExampleSensor1(Entity):
    """Representation of a sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Example Platform Sensor 2'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.hass.data[DOMAIN]['temperature']


class TrueNASSensor(Entity):
    # NOTE: https://github.com/home-assistant/core/blob/dev/homeassistant/components/plaato/sensor.py#L69
    """Representation of a sensor."""
    def __init__(self, arg1_config, arg_n, arg_x):
        """Initialize the sensor."""
        
        self._config = arg1_config
        self._static = arg_x
        self._arg_n = arg_n
        
        self._state = None
        self._connected = False
        self._cpu_temp = 0

        self._name = arg1_config.title
        
        # TODO: Keep learning
        # -ONE-:  self._devide_id = arg1_config["device_id"]
        # -TWO-:  self._devide_id = self._config["device_id"]
        # Try to use the variable value in a property will error -- CONF_DEVICE_ID is not defined
        # - See @property "state_attributes" -- NOTE: Set at top of file instead
        #CONF_DEVICE_ID = "device_id"
        #self._devide_id = arg1_config.data[CONF_DEVICE_ID]
        
        #self._config = arg1_config.data > Results is error > unable to serialize JSON: type mapping error
        #self._devide_id = arg1_config.options[CONF_DEVICE_ID]
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._cpu_temp
    
    @property
    def unique_id(self):
        return self._config.entry_id

    @property
    def state_attributes(self):
        """Return the state attributes of the sun."""
        return {
            "Title": self._config.title,
            "Arg N": self._arg_n,
            "Static (arg_x)": self._static,
            "Value": "Static value",
            
            "CPU Temp": self._cpu_temp,
            "STATE_ATTR_STATUS": self._connected,
            
            ## NOTE: After moving CONF_DEVICE_ID to top this works
            #CONF_DEVICE_ID: self._devide_id,
            #- "device_id": self._devide_id,
            
            ## NOTE: Helper attr to view config_entry
            "config": self._config
        }
        
        
    # https://developers.home-assistant.io/docs/entity_index#updating-the-entity
    # This is the only method that should fetch new data for Home Assistant.
    async def async_update(self):
        """ Fetch new state data for the sensor. """
        # TODO: Something relevant here... sync library or something
        #self._state = self.hass.data[GM_DOMAIN]['state']
        #self._connected = self.hass.data[DOMAIN]['connected']
        self._connected = self.hass.data[DOMAIN]['state'],
        self._cpu_temp = self.hass.data[DOMAIN]['temperature']
