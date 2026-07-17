"""SmartFarm orchestration module for multi-agent crop advisory system."""

try:
    from .agents import WeatherAgent, CropRiskAgent, DataAgent, AdvisorAgent, ReviewerAgent, ReportAgent
except ImportError:
    # Placeholder agents for development/testing
    class WeatherAgent:
        """Placeholder weather agent used when agent modules are unavailable."""

        def run(self, lat=None, lon=None, forecast_override=None):
            """Return a simple weather dict.

            Args:
                lat (float|None): latitude
                lon (float|None): longitude
                forecast_override (Any|None): optional override value for forecast

            Returns:
                dict: simple weather information
            """
            # basic behavior: prefer explicit override, then lat/lon, else unknown
            if forecast_override is not None:
                return {"weather": forecast_override}
            if lat is not None and lon is not None:
                return {"weather": f"unknown at {lat},{lon}"}
            return {"weather": "unknown"}

        def speak(self, weather):
                """Return a message for weather information using the provided value.

                Args:
                    weather (Any): weather information (typically a string)

                Returns:
                    str: human-readable weather message
                """
                return f"Weather: {weather}"

    class CropRiskAgent:
        """Placeholder crop risk agent used when agent modules are unavailable."""

        def run(self, weather, scenario=None):
            """Return crop risk assessment based on weather and scenario.

            Args:
                weather (Any): weather information
                scenario (dict|None): optional scenario data

            Returns:
                dict: risk assessment with 'risks' key
            """
            if weather is not None:
                _ = weather
            if scenario is not None:
                _ = scenario
            return {"risks": []}

        def speak(self, risks):
            """Return a message describing the computed risks.

            Args:
                risks (list): list of identified risks

            Returns:
                str: human-readable risk summary
            """
            if risks:
                return f"Risk assessment identified {len(risks)} issues."
            return "Risk assessment is not available."

    class DataAgent:
        """Placeholder data agent used when agent modules are unavailable."""

        def run(self, crop):
            """Return placeholder data for the given crop.

            Args:
                crop (Any): crop identifier or crop data.

            Returns:
                dict: placeholder USDA and World Bank data keyed by crop.
            """
            return {
                "usda_raw": {"crop": crop},
                "world_bank": {"crop": crop},
            }

        def speak(self, usda_raw, world_bank):
            """Generate a short human-readable summary from USDA and World Bank data.

            Args:
                usda_raw (dict): raw USDA data for the crop
                world_bank (dict): raw World Bank data for the crop

            Returns:
                str: brief summary string
            """
            # Safely extract a crop name or descriptor when available
            usda_crop = None
            wb_crop = None
            if isinstance(usda_raw, dict):
                usda_crop = usda_raw.get("crop")
            if isinstance(world_bank, dict):
                wb_crop = world_bank.get("crop")

            if usda_crop and wb_crop:
                if usda_crop == wb_crop:
                    return f"Data available for {usda_crop}."
                return f"USDA data for {usda_crop}; World Bank data for {wb_crop}."
            if usda_crop:
                return f"USDA data available for {usda_crop}."
            if wb_crop:
                return f"World Bank data available for {wb_crop}."
            return "Data summary is not available."

    class AdvisorAgent:
        """Placeholder advisor agent used when agent modules are unavailable."""

        def run(self, weather, risks, scenario=None):
            """Return a simple advisory recommendation based on weather, risks, and scenario.

            Args:
                weather (Any): weather information
                risks (list): list of identified risks
                scenario (dict|None): optional scenario data

            Returns:
                dict: recommendation summary
            """
            if risks:
                recommendation = "Monitor identified risks and adjust management practices."
            elif weather is not None:
                recommendation = f"Weather indicates {weather}; proceed with standard care."
            else:
                recommendation = "No recommendation available."

            if scenario and isinstance(scenario, dict) and scenario.get("forecast_override") is not None:
                recommendation += " Check overridden forecast assumptions."

            return {"recommendation": recommendation}

        def speak(self, recommendation):
            """Return the recommendation as-is.

            Args:
                recommendation (str): recommendation text

            Returns:
                str: the recommendation
            """
            return recommendation

    class ReviewerAgent:
        """Placeholder reviewer agent used when agent modules are unavailable."""

        def run(self, recommendation):
            """Return a basic review result for a recommendation.

            Args:
                recommendation (str): recommendation text

            Returns:
                dict: review output with an issues list
            """
            if recommendation is not None:
                _ = recommendation
            return {"issues": []}

        def speak(self, issues):
            """Return a placeholder review message.

            Args:
                issues (list): review issues to include in output

            Returns:
                str: placeholder review text
            """
            _ = issues
            return "Review is not available."

    class ReportAgent:
        """Placeholder report agent used when agent modules are unavailable."""

        def run(self, outputs):
            """Return a placeholder report record from agent outputs.

            Args:
                outputs (dict): composed agent outputs and voices

            Returns:
                dict: composed report output
            """
            return {
                "weather": outputs.get("weather"),
                "risks": outputs.get("risks"),
                "data": outputs.get("data"),
                "advice": outputs.get("advice"),
                "review": outputs.get("review"),
                "voices": {
                    "weather": outputs.get("weather_voice"),
                    "risk": outputs.get("risk_voice"),
                    "data": outputs.get("data_voice"),
                    "advisor": outputs.get("advisor_voice"),
                    "reviewer": outputs.get("reviewer_voice"),
                },
            }

        def speak(self, report):
            """Return a placeholder report summary.

            Args:
                report (dict): composed report output

            Returns:
                str: placeholder report text
            """
            _ = report
            return "Report summary is not available."


class SmartFarm:
    """
    SmartFarm Orchestrator — now supports full scenario objects.
    """

    def __init__(self, crop, location, scenario=None):
        """Initialize SmartFarm.

        location may be a (lat, lon) tuple/list or a dict with 'lat' and 'lon' keys,
        or any other descriptor. lat/lon will be extracted when available.
        """
        self.crop = crop
        self.location = location
        self.scenario = scenario or {}

        # extract lat/lon if provided in location to reduce positional args
        self.lat = None
        self.lon = None
        if isinstance(location, (tuple, list)) and len(location) >= 2:
            self.lat, self.lon = location[0], location[1]
        elif isinstance(location, dict):
            self.lat = location.get("lat")
            self.lon = location.get("lon")

        self.agents = {
            "weather": WeatherAgent(),
            "crop_risk": CropRiskAgent(),
            "data": DataAgent(),
            "advisor": AdvisorAgent(),
            "reviewer": ReviewerAgent(),
            "report": ReportAgent(),
        }

    def get_context(self):
        """Return the orchestration context for this SmartFarm instance."""
        return {
            "crop": self.crop,
            "location": self.location,
            "scenario": self.scenario,
            "lat": self.lat,
            "lon": self.lon,
        }

    def run(self):
        """Execute full multi-agent pipeline."""

        weather = self.agents["weather"].run(
            self.lat,
            self.lon,
            self.scenario.get("forecast_override")
        )
        weather_voice = self.agents["weather"].speak(weather["weather"])

        data = self.agents["data"].run(self.crop)
        data_voice = self.agents["data"].speak(data["usda_raw"], data["world_bank"])

        risks = self.agents["crop_risk"].run(weather["weather"], self.scenario)
        risk_voice = self.agents["crop_risk"].speak(risks["risks"])

        advice = self.agents["advisor"].run(weather["weather"], risks["risks"], self.scenario)
        advisor_voice = self.agents["advisor"].speak(advice["recommendation"])

        review = self.agents["reviewer"].run(advice["recommendation"])
        reviewer_voice = self.agents["reviewer"].speak(review["issues"])

        report = self.agents["report"].run(
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
