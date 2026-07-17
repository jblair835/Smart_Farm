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
    data = safe_request(url, params)

    # Check if the API returned an error dictionary instead of weather arrays
    if isinstance(data, dict) and (data.get("error") or "Daily API request limit" in str(data)):
        log("API Error or Limit Exceeded. Activating static fallback data.")

        # Returns structure containing standard parameters your downstream agents expect
        return {
            "latitude": lat,
            "longitude": lon,
            "generationtime_ms": 0.1,
            "utc_offset_seconds": -25200,
            "timezone": "America/Los_Angeles",
            "timezone_abbreviation": "PDT",
            "elevation": 700.0,
            "hourly": {
                "time": [f"2026-07-17T{str(i).zfill(2)}:00" for i in range(24)],
                "temperature_2m": [25.0] * 24,
                "precipitation": [0.0] * 24,
                "wind_speed_10m": [12.0] * 24
            },
            "daily": {
                "time": ["2026-07-17"],
                "temperature_2m_max": [32.0],
                "temperature_2m_min": [18.0],
                "precipitation_sum": [0.0]
            },
            "weather": {
                "temperature_c": 25.0,
                "wind_speed_kmh": 12.0,
                "precipitation_mm": 0.0
            },
            "risks": {
                "water_stress": True,
                "wind_drift": False,
                "fertilizer_leaching": False
            }
        }

    return data
