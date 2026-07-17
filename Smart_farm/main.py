class SmartFarm:
    """
    SmartFarm Orchestrator — now supports full scenario objects.
    """

    def __init__(self, crop, lat, lon, location, scenario=None):
        self.crop = crop
        self.lat = lat
        self.lon = lon
        self.location = location
        self.scenario = scenario or {}

        self.weather_agent = WeatherAgent()
        self.crop_risk_agent = CropRiskAgent()
        self.data_agent = DataAgent()
        self.advisor_agent = AdvisorAgent()
        self.reviewer_agent = ReviewerAgent()
        self.report_agent = ReportAgent()

    def run(self):
        """Execute full multi-agent pipeline."""

        # Weather
        weather = self.weather_agent.run(
            self.lat,
            self.lon,
            self.scenario.get("forecast_override")
        )
        weather_voice = self.weather_agent.speak(weather["weather"])

        # Data
        data = self.data_agent.run(self.crop)
        data_voice = self.data_agent.speak(data["usda_raw"], data["world_bank"])

        # Risks
        risks = self.crop_risk_agent.run(weather["weather"], self.scenario)
        risk_voice = self.crop_risk_agent.speak(risks["risks"])

        # Advisor
        advice = self.advisor_agent.run(weather["weather"], risks["risks"], self.scenario)
        advisor_voice = self.advisor_agent.speak(advice["recommendation"])

        # Reviewer
        review = self.reviewer_agent.run(advice["recommendation"])
        reviewer_voice = self.reviewer_agent.speak(review["issues"])

        # Final report
        report = self.report_agent.run(
            weather_output=weather,
            risk_output=risks,
            data_output=data,
            advisor_output=advice,
            reviewer_output=review,
            weather_voice=weather_voice,
            risk_voice=risk_voice,
            data_voice=data_voice,
            advisor_voice=advisor_voice,
            reviewer_voice=reviewer_voice
        )

        return report
