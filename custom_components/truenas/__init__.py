"""Example Load Platform integration."""

import asyncio
import logging

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .truenas_report_dev import HelloWorld

PLATFORMS = ["sensor"]

#SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    # Data that you want to share with your platforms
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up A Default Integration from a config entry."""

    host = entry.data[CONF_HOST]
    api_key = entry.data[CONF_API_KEY]

    coordinator = TrueNASDataUpdateCoordinator(hass, host=host, api_key=api_key)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    # Store an API object for your platforms to access
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            [
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


class TrueNASDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from TrueNAS."""
    def __init__(self, hass, host, api_key):
        """Initialize."""
        self._api = HelloWorld(host, api_key)
        super().__init__(
            #hass,_LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL,
            hass,_LOGGER, name=DOMAIN,
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            #await self._api.async_refresh_data() <-- WARNING: I/O inside the event loop
            await self.hass.async_add_executor_job(self._api.refresh_data)
        except ConnectionError as error:
            raise UpdateFailed(error)
        
        _LOGGER.debug(f'update from TrueNAS: {self._api.data}')

        return self._api.data
