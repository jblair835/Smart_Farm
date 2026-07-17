#-----------------------
# OpenAQ
#-----------------------
"""OpenAQ API integration for Smart Farm project."""

from agents.tools.utils.error_handler import safe_request
from agents.tools.utils.logger import log
from agents.tools.utils.cache import cache_result

@cache_result(ttl=3600)
def get_air_quality(city="Bakersfield"):
    """Fetch air‑quality data from OpenAQ API."""
    url = "https://api.openaq.org/v2/latest"
    params = {"city": city}
    log(f"Fetching air quality data for {city}")
    return safe_request(url, params)
