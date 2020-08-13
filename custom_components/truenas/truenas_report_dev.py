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
    # TODO replace with a transport adapter, timeouts + retry on failure
    # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
    
    errors = {}
    
    cto = 1   # connection timeout
    rto = 60  # read timeout
    
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Home Assistant',
      'Authorization': 'Bearer ' + self._api_key
    }
    
    try:
      response = get(f'{self._host}/api/v2.0/{path}', headers=headers, timeout=(cto,rto))
      if response.status_code != 200:
        _LOGGER.warning(f'ERROR {response.status_code}: {response.text}')
        # FIXME data = dict(status: code, attrubute: respons.text)
        data = response.status_code
      else:
        data = response.json()
        _LOGGER.debug(f'api data: {response.text}')
      return data
    
    except:
      _LOGGER.error("API FUNCTION ERROR: unknown exception")

    # TODO finally: return dict(status: code, attrubute: respons.text)
    return "ERROR"


  def refresh_data(self):  # pylint:disable=too-many-branches
    """Update data from printer."""
    data = {}
    sys_state = self.get_system_state()
    if not sys_state or sys_state == "ERROR":
      # self.data = {}
      self.data = {"system_state": sys_state}
      return

    sys_info = dict(self.get_system_info())

    data = {
      "system_state": sys_state,
      "uptime": sys_info['uptime'],
      "system_info": sys_info,
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


  def get_system_info(self):
    """ get TrueNAS system info """
    return self.api('GET', '/system/info')


  def get_system_state(self):
    """Returns system state: 
    "BOOTING" - System is booting
    "READY" - System completed boot and is ready to use
    "SHUTTING_DOWN" - System is shutting down"""
    return self.api('GET', '/system/state')


  def get_system_ready(self):
    """Returns 'true' if system completed boot and is ready to use."""
    return self.api('GET', '/system/ready')

  @property
  def available(self):
      """Return True is data is available."""
      return bool(self.data)
