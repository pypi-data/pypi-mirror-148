"""
freegeoip_client package.

Provides FreeGeoIpClient object which enables consuming
FreeGeoIp's RESTful API by providing your own API key.

Usage
-----
from freegeoip_client import FreeGeoIpClient

client = FreeGeoIpClient(api_key="some_api_key")

geo_data = client.get_geo_location()
geo_data_by_ip = client.get_geo_location_for_ip_address("8.8.8.8")
"""

from .client import FreeGeoIpClient  # noqa: F401
