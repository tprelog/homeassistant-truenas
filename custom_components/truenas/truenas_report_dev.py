import logging
from datetime import datetime, timedelta

import requests
from requests import get

#from .const import *

_LOGGER = logging.getLogger(__name__)

class HelloWorld():
  def __init__(self, host, api_key):

    self.data = {}
    self._host = host
    self._api_key = api_key


  def api(self, action, path, payload=None):
    """ return an api endpoint as url """
    errors = {}
    
    cto = 1   # connection timeout
    rto = 60  # read timeout
    
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Home Assistant',
      'Authorization': 'Bearer ' + self._api_key
    }
    
    try:
      response = get(f'{self._host}/api/v2.0/{path}', headers=headers, timeout=(cto, rto))
      if response.status_code != 200:
        _LOGGER.info(f'ERROR {response.status_code}: {response.text}')
        data = response.status_code
      else:
        data = response.json()
        _LOGGER.info(f'system/state: {response.text}')
      return data
    
    except:
      _LOGGER.error("API FUNCTION ERROR: unknown exception")
      _LOGGER.debug(f'{response.text}')
    return "SHIT"


  def get_system_state(self):
    return self.api('get', '/system/state')




  def refresh_data(self):  # pylint:disable=too-many-branches
    """Update data from printer."""

    raw_data = self.get_system_state()

    if not raw_data:
      self.data = {}
      return

    _LOGGER.debug(f'refresh_data_received: {raw_data}')

    data = {}
    data = {
      "sensor_name": "Hello World",
      "device_class": "temperature",
      "unit_of_measurement": '°C',
      "cpu_temp": 0,
      "count": self.timestamp()
      }
    
    self.data = data


  def timestamp(self):
    """ return epoch timestamp """
    now = datetime.now()
    return round(datetime.timestamp(now))

  @property
  def available(self):
      """Return True is data is available."""
      return bool(self.data)
