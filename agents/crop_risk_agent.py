# agents/crop_risk_agent.py

class CropRiskAgent:
    """
    Detects all agricultural risks using weather + farm conditions.
    Rusty provides persona-rich commentary.
    """

    def run(self, weather, scenario):
        risks = []

        # Heat stress
        if weather["day1"]["temp_c"] >= 38 or weather["day2"]["temp_c"] >= 38:
            risks.append("Heat stress risk due to high temperatures.")

        # Water stress
        last_irrigation = scenario.get("last_irrigation_days")
        if last_irrigation is None:
            last_irrigation = 0

        if scenario["soil_moisture"] == "Low" or last_irrigation >= 4:
            risks.append("Water stress likely due to low moisture or delayed irrigation.")

        # Wind drift risk
        if weather["day1"]["wind_kmh"] >= 25:
            risks.append("High wind drift risk — avoid spraying today.")

        return {"risks": risks}

    def speak(self, risks):
        if not risks:
            return "Rusty says: No major risks today — you're in good shape."
        return "Rusty says:\n- " + "\n- ".join(risks)
