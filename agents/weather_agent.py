# agents/weather_agent.py

import requests

class WeatherAgent:
    """
    Fetches 3-day weather forecast from Open-Meteo
    and formats it for SmartFarmBrain.
    """

    def run(self, lat, lon, override=None):
        # If user provided a custom forecast, use it
        if override:
            return {
                "agent": "Weather Agent",
                "weather": override
            }

        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&daily=temperature_2m_max,precipitation_sum,wind_speed_10m_max"
            "&timezone=America/Los_Angeles"
        )

        data = requests.get(url).json()
        daily = data["daily"]

        return {
            "agent": "Weather Agent",
            "weather": {
                "day1": {
                    "temp_c": daily["temperature_2m_max"][0],
                    "rain_mm": daily["precipitation_sum"][0],
                    "wind_kmh": daily["wind_speed_10m_max"][0],
                },
                "day2": {
                    "temp_c": daily["temperature_2m_max"][1],
                    "rain_mm": daily["precipitation_sum"][1],
                    "wind_kmh": daily["wind_speed_10m_max"][1],
                },
                "day3": {
                    "temp_c": daily["temperature_2m_max"][2],
                    "rain_mm": daily["precipitation_sum"][2],
                    "wind_kmh": daily["wind_speed_10m_max"][2],
                }
            }
        }

    def speak(self, weather, prompt=None):
        return (
            f"Clara says: Day 1 will be {weather['day1']['temp_c']}°C with "
            f"{weather['day1']['rain_mm']}mm rain and {weather['day1']['wind_kmh']} km/h wind."
        )
