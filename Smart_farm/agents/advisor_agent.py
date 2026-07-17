# agents/advisor_agent.py

class AdvisorAgent:
    """
    Makes decisions: irrigation, pesticide, fertilizer.
    Ranks priorities. Doc provides persona-rich advice.
    """

    def run(self, weather, risks, scenario):
        decisions = {}

        # --- Irrigation ---
        if risks["water_stress"]:
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
        if risks["wind_drift"]:
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
        if risks["fertilizer_leaching"]:
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
        for name, d in decisions.items():
            lines.append(
                f"\n{name.title()} — {'YES' if d.get('should_irrigate') or d.get('should_spray') or d.get('should_apply') else 'NO'}"
                f"\n• Timing: {d['timing']}"
                f"\n• Reason: {d['reason']}"
                f"\n• Priority: {d['priority']}"
            )
        return "\n".join(lines)
