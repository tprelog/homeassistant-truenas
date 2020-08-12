import json

from datetime import datetime, timedelta
from requests import get, post


class HelloWorld():
  def __init__(self, host, api_key):

    self.data = {}
    self._host = host
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Home Assistant',
      'Authorization': 'Bearer ' + api_key
    }
    
  async def async_update(self):
      
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
        return True
