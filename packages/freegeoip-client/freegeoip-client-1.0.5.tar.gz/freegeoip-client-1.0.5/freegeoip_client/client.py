from configparser import ConfigParser
from typing import Dict, Any

import requests
from pkg_resources import resource_filename


class FreeGeoIpClient:
    """
    A class which enables consuming Freegeoip's RESTful API.

    Attributes
    ----------
    api_key : str
        provides API required to fetch data.
    api_endpoint : str
        stores API endpoint.

    Methods
    -------
    get_geo_location():
        Returns geo data for current location based on IP address that made the request.
    get_geo_location_for_ip_address(ip_address):
        Returns geo data for location based on provided IP address.
    """

    def __init__(self, api_key) -> None:
        """
        Constructs all the necessary attributes for the Client object.

        Parameters
        ----------
        api_key : str
            Freegeoip's API key.
        """
        self.api_key = api_key
        self.api_endpoint = self.get_api_endpoint

    @property
    def get_api_endpoint(self) -> str:
        """
        Returns
        -------
        API endpoint : str
            Freegeoip's API endpoint.
        """
        return self.__get_config_file()["API"]["ENDPOINT"]

    def __get_config_file(
        self,
        filename: str = resource_filename(__name__, "data/client.cfg"),
    ) -> ConfigParser:
        """
        Get contents of config file.

        Parameters
        ----------
        filename : str
            Config file to read.

        Returns
        -------
        config : ConfigParser
            contents of config file.
        """
        config = ConfigParser()
        config.read(filename)
        return config

    def get_geo_location(self) -> Dict[str, Any]:
        """
        Get geo data for current location based on IP address that made the request.

        Returns
        -------
        geo data : Dict[str, Any]
            geo data for current location.

        Raises
        ------
        JSONDecodeError, HTTPError, MissingSchema
        """
        return requests.get(f"{self.api_endpoint}/?apikey={self.api_key}").json()

    def get_geo_location_for_ip_address(
        self,
        ip_address: str,
    ) -> Dict[str, Any]:
        """
        Get geo data for location based on provided IP address.

        Parameters
        ----------
        ip_address : str
            Desired IP address.

        Returns
        -------
        geo data : Dict[str, Any]
            geo data for location based on provided IP address.

        Raises
        ------
        JSONDecodeError, HTTPError, MissingSchema
        """
        return requests.get(
            f"{self.api_endpoint}/{ip_address}?apikey={self.api_key}"
        ).json()


if __name__ == "__main__":
    pass
