"""Advisor agent for making farm recommendations."""


class AdvisorAgent:
    """
    Makes decisions: irrigation, pesticide, fertilizer.
    Ranks priorities. Doc provides persona-rich advice.
    """

    def run(self, weather, risks, _scenario):
        """Generate farm recommendations based on weather and risk conditions."""
        # Ensure we reference `weather` to avoid unused-argument warnings.
        # Accepts dict-like weather with optional 'rain_mm' or 'rain_expected' keys.
        if isinstance(weather, dict):
            rain_mm = weather.get("rain_mm") if weather.get("rain_mm") is not None else (
                5 if weather.get("rain_expected") else 0
            )
        else:
            rain_mm = 0

        decisions = {}

        # --- Irrigation ---
        # If rain is imminent, deprioritize irrigation even with water stress
        if risks.get("water_stress") and (rain_mm == 0 or rain_mm < 2):
            decisions["irrigation"] = {
                "should_irrigate": True,
                "timing": "Evening of Day 1 (cooler temps, less evaporation)",
                "reason": "Soil moisture is low and last irrigation was 5 days ago.",
                "priority": 1
            }
        else:
            decisions["irrigation"] = {
                "should_irrigate": False,
                "timing": None,
                "reason": "Moisture adequate.",
                "priority": 3
            }

        # --- Pesticide ---
        if risks.get("wind_drift"):
            decisions["pesticide"] = {
                "should_spray": False,
                "timing": "Delay until wind < 15 km/h",
                "reason": "High wind increases drift risk.",
                "priority": 2
            }
        else:
            decisions["pesticide"] = {
                "should_spray": True,
                "timing": "Morning Day 1",
                "reason": "Wind acceptable.",
                "priority": 4
            }

        # --- Fertilizer ---
        # If light rain is expected (under ~2 mm) it's safe to apply;
        # heavy rain increases leaching risk
        if risks.get("fertilizer_leaching") or (rain_mm and rain_mm >= 5):
            decisions["fertilizer"] = {
                "should_apply": False,
                "timing": "After Day 3 rainfall",
                "reason": "Heavy rain may wash fertilizer away.",
                "priority": 3
            }
        else:
            decisions["fertilizer"] = {
                "should_apply": True,
                "timing": "Day 2",
                "reason": "No major rainfall expected.",
                "priority": 5
            }

        return {"recommendation": decisions}

    def speak(self, decisions):
        """Persona output from Doc."""
        lines = ["Here’s the plan, straight from Doc:"]

        key_map = {
            "irrigation": "should_irrigate",
            "pesticide": "should_spray",
            "fertilizer": "should_apply"
        }

        for name, d in decisions.items():
            action_key = key_map.get(name)
            is_active = d.get(action_key, False) if action_key else False
            yes_no = "YES" if is_active else "NO"

            lines.append(
                f"\n{name.title()} — {yes_no}"
                f"\n• Timing: {d.get('timing')}"
                f"\n• Reason: {d.get('reason')}"
                f"\n• Priority: {d.get('priority')}"
            )

        return "\n".join(lines)
