"""Example Load Platform integration."""
import asyncio
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.const import (
    CONF_API_KEY,
    CONF_HOST,
)

from .const import (
    DOMAIN,
    STATE_ATTR_STATUS,
    STATE_ATTR_VERSION,
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    # Data that you want to share with your platforms
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up A Default Integration from a config entry."""

    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    hass.data[DOMAIN] = {
        'system': entry.title,
        STATE_ATTR_STATUS: "READY",
        'cpu_temp': 15
    }

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    #if unload_ok:
    #    hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
