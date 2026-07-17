# agents/crop_risk_agent.py
"""
Crop risk detection agent for agricultural scenario analysis.
Analyzes weather and farm conditions to identify potential risks.
"""


class CropRiskAgent:
    """
    Detects agricultural risks using weather + farm conditions.
    Rusty provides persona-rich commentary.
    """

    def run(self, weather, scenario):
        """Analyze weather and farm scenario to identify crop risks."""
        risks = []

        # If weather is missing or errored, return no weather-based risks
        if not weather or not isinstance(weather, dict):
            return {"risks": ["Weather data unavailable — skipping weather-based risk analysis."]}

        # Extract days safely
        day1 = weather.get("day1", {})
        day2 = weather.get("day2", {})

        temp1 = day1.get("temp_c")
        temp2 = day2.get("temp_c")
        wind1 = day1.get("wind_kmh")

        # --- Heat stress ---
        if (temp1 is not None and temp1 >= 38) or (temp2 is not None and temp2 >= 38):
            risks.append("Heat stress risk due to high temperatures.")

        # --- Water stress ---
        last_irrigation = scenario.get("last_irrigation_days")
        if last_irrigation is None:
            last_irrigation = 0

        soil_moisture = scenario.get("soil_moisture", "Unknown")

        if soil_moisture == "Low" or last_irrigation >= 4:
            risks.append("Water stress likely due to low moisture or delayed irrigation.")

        # --- Wind drift risk ---
        if wind1 is not None and wind1 >= 25:
            risks.append("High wind drift risk — avoid spraying today.")

        return {"risks": risks}

    def speak(self, risks):
        """Return a user-friendly summary of detected risks."""
        if not risks:
            return "Rusty says: No major risks today — you're in good shape."

        return "Rusty says:\n- " + "\n- ".join(risks)
