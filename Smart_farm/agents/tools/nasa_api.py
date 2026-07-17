#-----------------------
# NASA
#-----------------------
"""NASA API integration for Smart Farm project."""

from agents.tools.utils.error_handler import safe_request
from agents.tools.utils.logger import log
from agents.tools.utils.cache import cache_result

@cache_result(ttl=86400)
def get_nasa_data(api_key="YOUR_NASA_API_KEY"):
    """Access NASA Earth Data (Astronomy Picture of the Day example)."""
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key}
    log("Fetching NASA APOD data")
    return safe_request(url, params)
