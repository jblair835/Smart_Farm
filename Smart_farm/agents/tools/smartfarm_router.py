# agents/tools/smartfarm_router.py

class SmartFarmRouter:
    """
    NLP-aware router that decides whether a prompt should:
    - Use SmartFarmBrain (full advisory)
    - Use WeatherAgent (simple weather Q&A)
    - Use USDAAgent (simple yield Q&A)
    """

    def __init__(self):
        from agents.weather_agent import WeatherAgent
        from agents.usda_agent import USDAAgent

        self.weather = WeatherAgent()
        self.usda = USDAAgent()

    def route(self, prompt: str) -> str:
        p = prompt.lower()

        advisory_keywords = [
            "irrigation", "fertilizer", "pesticide", "spray",
            "growth stage", "soil moisture", "acres",
            "next 72 hours", "what should i do", "recommend",
            "risk", "operational", "plan", "schedule",
            "should i", "i have enough water", "my farm"
        ]
        if any(word in p for word in advisory_keywords):
            return "brain"

        weather_keywords = [
            "weather", "rain", "wind", "temperature", "forecast",
            "hot", "cold", "storm", "humidity"
        ]
        if any(word in p for word in weather_keywords):
            return "weather"

        usda_keywords = [
            "yield", "production", "harvest", "acre", "usda"
        ]
        if any(word in p for word in usda_keywords):
            return "usda"

        return "brain"

    def handle(self, prompt: str, lat=None, lon=None):
        agent_name = self.route(prompt)

        if agent_name == "weather":
            data = self.weather.run(lat, lon)
            return self.weather.speak(data["weather"], prompt)

        if agent_name == "usda":
            data = self.usda.run(prompt)
            return self.usda.speak(data["usda"], prompt)

        # Lazy import to avoid circular dependency
        from agents.tools.smartfarm_brain import SmartFarmBrain
        brain = SmartFarmBrain()
        return brain.ask(prompt, lat, lon)
