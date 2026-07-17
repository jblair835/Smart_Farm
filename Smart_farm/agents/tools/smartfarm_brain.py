# agents/tools/smartfarm_brain.py

import re
from agents.weather_agent import WeatherAgent
from agents.crop_risk_agent import CropRiskAgent
from agents.advisor_agent import AdvisorAgent
from agents.reviewer_agent import ReviewerAgent
from agents.report_agent import ReportAgent

class SmartFarmBrain:
    """
    Natural-language farm intelligence engine.
    """

    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.crop_risk_agent = CropRiskAgent()
        self.advisor_agent = AdvisorAgent()
        self.reviewer_agent = ReviewerAgent()
        self.report_agent = ReportAgent()

    def parse_prompt(self, prompt: str):
        prompt = prompt.lower()

        crops = ["tomatoes", "corn", "wheat", "alfalfa", "grapes", "cotton",
                 "lettuce", "oranges", "strawberries", "peaches", "rice",
                 "soybeans", "barley", "oats", "sorghum", "hay", "beans",
                 "potatoes", "onions", "garlic"]
        crop = next((c.upper() for c in crops if c in prompt), "TOMATOES")

        stages = ["flowering", "vegetative", "fruiting", "harvest"]
        growth_stage = next((s.title() for s in stages if s in prompt), "Unknown")

        farm_size_match = re.search(r"(\d+)\s*acres", prompt)
        farm_size = int(farm_size_match.group(1)) if farm_size_match else None

        if "low moisture" in prompt:
            soil_moisture = "Low"
        elif "medium moisture" in prompt:
            soil_moisture = "Medium"
        elif "high moisture" in prompt:
            soil_moisture = "High"
        else:
            soil_moisture = "Unknown"

        irr_match = re.search(r"(\d+)\s*days ago", prompt)
        last_irrigation_days = int(irr_match.group(1)) if irr_match else None

        pesticide_day = 1 if "pesticide" in prompt or "spray" in prompt else None
        fertilizer_day = 2 if "fertilizer" in prompt else None

        forecast_override = None
        if "day 1" in prompt and "day 2" in prompt and "day 3" in prompt:
            forecast_override = {
                "day1": {
                    "temp_c": self.extract_temp(prompt, "day 1"),
                    "rain_mm": self.extract_rain(prompt, "day 1"),
                    "wind_kmh": self.extract_wind(prompt, "day 1")
                },
                "day2": {
                    "temp_c": self.extract_temp(prompt, "day 2"),
                    "rain_chance": self.extract_rain_chance(prompt, "day 2")
                },
                "day3": {
                    "temp_c": self.extract_temp(prompt, "day 3"),
                    "rain_mm": self.extract_rain(prompt, "day 3")
                }
            }

        return {
            "crop": crop,
            "growth_stage": growth_stage,
            "farm_size": farm_size,
            "soil_moisture": soil_moisture,
            "last_irrigation_days": last_irrigation_days,
            "planned_ops": {
                "pesticide_day": pesticide_day,
                "fertilizer_day": fertilizer_day
            },
            "forecast_override": forecast_override
        }

    def extract_temp(self, prompt, day):
        m = re.search(fr"{day}:\s*(\d+)\s*°?c", prompt)
        return int(m.group(1)) if m else None

    def extract_rain(self, prompt, day):
        m = re.search(fr"{day}:\s*\d+°c,\s*(\d+)\s*mm", prompt)
        return int(m.group(1)) if m else 0

    def extract_wind(self, prompt, day):
        m = re.search(fr"{day}:\s*\d+°c,\s*\d+\s*mm rain,\s*wind\s*(\d+)\s*km/h", prompt)
        return int(m.group(1)) if m else None

    def extract_rain_chance(self, prompt, day):
        m = re.search(fr"{day}:\s*\d+°c,\s*(\d+)%", prompt)
        return int(m.group(1)) / 100 if m else None

    def ask(self, prompt: str, lat=None, lon=None):
        # Lazy import — prevents circular dependency
        from agents.tools.smartfarm_router import SmartFarmRouter
        router = SmartFarmRouter()

        scenario = self.parse_prompt(prompt)

        weather = self.weather_agent.run(lat, lon, scenario["forecast_override"])
        weather_voice = self.weather_agent.speak(weather["weather"])

        risks = self.crop_risk_agent.run(weather["weather"], scenario)
        risk_voice = self.crop_risk_agent.speak(risks["risks"])

        decisions = self.advisor_agent.run(weather["weather"], risks["risks"], scenario)
        advisor_voice = self.advisor_agent.speak(decisions["recommendation"])

        review = self.reviewer_agent.run(decisions["recommendation"])
        reviewer_voice = self.reviewer_agent.speak(review["issues"])

        final = self.report_agent.run(
            weather_output=weather,
            risk_output=risks,
            data_output={},
            advisor_output=decisions,
            reviewer_output=review,
            weather_voice=weather_voice,
            risk_voice=risk_voice,
            data_voice="(USDA data optional)",
            advisor_voice=advisor_voice,
            reviewer_voice=reviewer_voice
        )

        return self.report_agent.speak(final["formatted"])
