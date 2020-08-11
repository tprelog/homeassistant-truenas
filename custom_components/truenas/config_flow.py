"""Config flow for Example integration."""
import logging
import time

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.core import callback

import homeassistant.helpers.config_validation as cv

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("host"): str,
        vol.Required("api_key"): str,
    }
)

class PlaceholderHub:
    """Placeholder class to make tests pass.
    TODO Remove this placeholder class and replace with things from your PyPI package.
    """
    def __init__(self, name):
        """Initialize."""
        self._name = name

    #async def authenticate(self, username, password) -> bool:
    async def authenticate(self, name) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )
    
    hub = PlaceholderHub(data["name"])

    #if not await hub.authenticate(data["username"], data["password"]):
    if not await hub.authenticate(data["name"]):
        raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": "Name of the device"}
    
#
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
#   CONFIG FLOW:
# - https://developers.home-assistant.io/docs/config_entries_config_flow_handler#defining-steps
#
#   DATA FLOW ENTRY --> https://developers.home-assistant.io/docs/data_entry_flow_index
# ---------------------------------------------------------------------------------------------
#
@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Example."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    # (this is not implemented yet)
    VERSION = 1
    
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    
    ## user initiated -- step 1
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            """TODO - actually validate something"""
            pass

            try: 
                await self.async_set_unique_id(time.time_ns())
                return self.async_create_entry(
                    title = user_input["name"],
                    data = {
                        "host": user_input["host"],
                        "api_key": user_input["api_key"]
                    }
                )            
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"


        ## show user initiated form - step 1
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
    

    # CALLBACK FOR OPTIONS FLOWS
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)
#
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
#   OPTIONS FLOW:
# - https://developers.home-assistant.io/docs/config_entries_options_flow_handler#options-support
#
#   DATA FLOW ENTRY --> https://developers.home-assistant.io/docs/data_entry_flow_index
# ---------------------------------------------------------------------------------------------
#
class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_options_1()
 
    async def async_step_options_1(self, user_input=None):
        """Manage the options."""

        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()
        
        return self.async_show_form(
            step_id = "options_1",
            data_schema = vol.Schema(
                {
                    vol.Optional(
                        "host",
                        default=self.config_entry.data.get('host', "http://TrueNaS.local"),
                        ): str,
                    vol.Optional(
                        "refresh",
                        default=self.config_entry.options.get('refresh', "60"),
                        ): str,
                    vol.Optional(
                        "enable_something",
                        default=self.config_entry.options.get('enable_something', True),
                        ): bool
                }
            )
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(title="", data=self.options)

#
#
# -------------------------------------------------------
# -------------------------------------------------------
#       """Default entries from scaffold"""

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""

# -------------------------------------------------------
# -------------------------------------------------------
#
#
