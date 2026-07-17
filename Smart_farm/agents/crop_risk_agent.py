# agents/crop_risk_agent.py

class CropRiskAgent:
    """
    Detects all agricultural risks using weather + farm conditions.
    Rusty provides persona-rich commentary.
    """

    def run(self, weather, scenario):
        risks = {}

        # Heat stress
        if weather["day1"]["temp_c"] >= 38 or weather["day2"]["temp_c"] >= 38:
            risks["heat_stress"] = True

        # Water stress
        if scenario["soil_moisture"] == "Low" or scenario["last_irrigation_days"] >= 4:
            risks["water_stress"] = True

        # Wind drift risk
        if weather["day1"]["wind_kmh"] >= 25:
            risks["wind_drift"] = True

        # Fertilizer leaching
        if weather["day3"].get("rain_mm", 0) >= 10:
            risks["fertilizer_leaching"] = True

        # Disease risk from rainfall + heat
        if weather["day3"].get("rain_mm", 0) >= 10 and weather["day1"]["temp_c"] >= 35:
            risks["disease_risk"] = True

        # Operational conflicts
        ops_conflicts = []
        if scenario["planned_ops"]["pesticide_day"] == 1 and weather["day1"]["wind_kmh"] >= 25:
            ops_conflicts.append("High wind makes pesticide spraying unsafe.")
        if scenario["planned_ops"]["fertilizer_day"] == 2 and weather["day3"].get("rain_mm", 0) >= 10:
            ops_conflicts.append("Heavy rain may wash away fertilizer.")

        risks["operational_conflicts"] = ops_conflicts

        return {"risks": risks}

    def speak(self, risks):
        """Persona output from Rusty."""
        lines = ["Rusty’s take — here’s what I see:"]
        for k, v in risks.items():
            if v:
                lines.append(f"• {k.replace('_', ' ').title()} detected")
        return "\n".join(lines)
