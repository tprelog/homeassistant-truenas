"""Example Load Platform integration."""
import asyncio
import logging

import voluptuous as vol

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    STATE_ATTR_STATUS,
    STATE_ATTR_VERSION,
)

from .truenas_report_v1 import HelloWorld

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    # Data that you want to share with your platforms
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up A Default Integration from a config entry."""

    host = entry.data[CONF_HOST]
    api_key = entry.data['api_key']
    #kind = entry.data[CONF_TYPE]

    coordinator = TrueNASDataUpdateCoordinator(hass, host=host, api_key=api_key)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    # Store an API object for your platforms to access
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Data that you want to share with your platforms
    # Do I set values using results from the coordinator
    # Do I remove this and pass coordinator.something to platform setup

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
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class TrueNASDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching TrueNAS data from the printer."""

    def __init__(self, hass, host, api_key):
        """Initialize."""
        self._TrueNAS = HelloWorld(host, api_key)
        super().__init__(
            hass,_LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL,
            #hass,_LOGGER, name=DOMAIN,
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            await self._TrueNAS.async_update()

        except ConnectionError as error:
            raise UpdateFailed(error)

        _LOGGER.info(f'update from TrueNAS: {self._TrueNAS.data}')

        return self._TrueNAS.data
