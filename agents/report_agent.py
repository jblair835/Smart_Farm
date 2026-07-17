# agents/report_agent.py
class ReportAgent:
    """
    Produces final structured farm report.
    Sage provides persona-rich summary.
    """

    def run(self, *args, **kwargs) -> dict[str, str]:
        """Produce the final structured farm report."""
        # Support legacy positional voice inputs and keyword voice inputs.
        if args and not kwargs:
            weather_voice, risk_voice, data_voice, advisor_voice, reviewer_voice = (
                list(args[:5]) + [None] * 5
            )[:5]
        else:
            weather_voice = kwargs.get("weather_voice")
            risk_voice = kwargs.get("risk_voice")
            data_voice = kwargs.get("data_voice")
            advisor_voice = kwargs.get("advisor_voice")
            reviewer_voice = kwargs.get("reviewer_voice")

        weather_voice = weather_voice or "Weather data unavailable."
        risk_voice = risk_voice or "No risk data available."
        data_voice = data_voice or "(No USDA data provided.)"
        advisor_voice = advisor_voice or "No recommendations available."
        reviewer_voice = reviewer_voice or "No review notes available."

        formatted = f"""
Sage reporting — here’s your real-time farm intelligence:

### 🌦 Weather Summary
{weather_voice}

### ⚠️ Risk Assessment
{risk_voice}

### 📊 Data Summary
{data_voice}

### 🧑‍🌾 Recommendations
{advisor_voice}

### 🔍 Review Notes
{reviewer_voice}
"""

        return {"formatted": formatted}

    def speak(self, formatted):
        return formatted
