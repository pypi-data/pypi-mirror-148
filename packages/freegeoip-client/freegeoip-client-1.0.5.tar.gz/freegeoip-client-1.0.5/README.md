# Description

Simple Python library made for consuming [FreeGeoIp's](https://freegeoip.app/) RESTful API. API returns geo location data either for
the current IP address that made the request or for the provided IP address.

## Installing and usage

Install using pip (available at [pypi - freegeoip-client](https://pypi.org/project/freegeoip-client/))

```bash
pip install freegeoip-client
```

Use it in code

```python
from freegeoip_client import FreeGeoIpClient

client = FreeGeoIpClient(api_key="some_api_key")

geo_data = client.get_geo_location()
geo_data_by_ip = client.get_geo_location_for_ip_address("8.8.8.8")
```

Example output

```python
>>> from freegeoip_client import FreeGeoIpClient
>>> client = FreeGeoIpClient(api_key="some_api_key")
>>> client.get_geo_location_for_ip_address("8.8.8.8")
{'ip': '8.8.8.8', 'country_code': 'US', 'country_name': 'United States', 'region_code': '', 'region_name': '', 'city': '', 'zip_code': '', 'time_zone': 'America/Chicago', 'latitude': 37.751, 'longitude': -97.822, 'metro_code': 0}
```

## Building project locally

Using [pip - Package Installer for Python](https://pip.pypa.io/en/stable/) and `setup.py`, `__init__.py` files to define which modules will be included in a package, project can be built and installed locally in order to import it in another Python script.

```bash
# OS-level (/usr/local/lib/<python version>)
python -m pip install -e .

# for current user (/home/<user>)
python -m pip install --user -e .

# virtual environment (wherever virtual environment is initialized)
python -m venv env
source /env/bin/activate
python -m pip install -e .
```

Importing in different script(s):

```python
from freegeoip_client import FreeGeoIpClient
```

## Third party dependencies for project development

Required:

- [requests](https://docs.python-requests.org/en/latest/) - Required to make HTTP requests

Not required (but highly encouraged to improve code quality):

- [flake8](https://flake8.pycqa.org/en/latest/) - Tool to enforce style guide for Python code ([PEP8](https://www.python.org/dev/peps/pep-0008/))
- [black](https://github.com/psf/black) - tool to format Python code
- [pytest](https://docs.pytest.org/en/7.0.x/) - framework for writing small and readable tests
- [requests-mock](https://requests-mock.readthedocs.io/en/latest/overview.html) - library at its core is simply a transport adapter that can be preloaded with responses that are returned if certain URIs are requested

Dependencies are defined in `requirements.txt` file and are installed using [pip](https://pip.pypa.io/en/stable/). Dependencies can be installed on OS-level, for current user or within virtual environments.

```bash
# OS-level (/usr/local/lib/<python version>)
python -m pip install -r requirements.txt

# for current user (/home/<user>)
python -m pip install --user -r requirements.txt

# virtual environment (wherever virtual environment is initialized)
python -m venv env
source /env/bin/activate
python -m pip install -r requirements.txt
```
