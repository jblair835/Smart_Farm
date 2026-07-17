"""Advisor agent for making farm recommendations."""

# agents/advisor_agent.py
class AdvisorAgent:
    """
    Makes decisions: irrigation, pesticide, fertilizer.
    Ranks priorities. Doc provides persona-rich advice.
    """

    def run(self, risks, _scenario):
        """Make decisions based on detected risks: irrigation, pesticide, fertilizer."""
        decisions = {}

        # --- Irrigation ---
        if risks.get("water_stress"):
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
        if risks.get("fertilizer_leaching"):
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
            # Dynamically look up the correct boolean flag based on the category name
            key_map = {
                "irrigation": "should_irrigate",
                "pesticide": "should_spray",
                "fertilizer": "should_apply"
            }
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
