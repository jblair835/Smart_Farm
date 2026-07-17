#-----------------------
# USGS Earthquake
#-----------------------
"""USGS Earthquake API integration for Smart Farm project."""

from agents.tools.utils.error_handler import safe_request
from agents.tools.utils.logger import log
from agents.tools.utils.cache import cache_result

@cache_result(ttl=86400)
def get_earthquake_data(start="2024-01-01", end="2024-12-31", min_mag=3):
    """Retrieve earthquake data from USGS Earthquake API."""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start,
        "endtime": end,
        "minmagnitude": min_mag
    }
    log(f"Fetching earthquake data from {start} to {end}, min magnitude {min_mag}")
    return safe_request(url, params)
