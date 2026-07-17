#-----------------------
# Open‑Meteo
#-----------------------
"""Open‑Meteo API integration for Smart Farm project."""

from agents.tools.utils.error_handler import safe_request
from agents.tools.utils.logger import log
from agents.tools.utils.cache import cache_result

@cache_result(ttl=600)
def get_weather(lat, lon):
    """Fetch weather forecast data from Open‑Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "America/Los_Angeles"
    }
    log(f"Fetching weather data for lat={lat}, lon={lon}")
    return safe_request(url, params)
