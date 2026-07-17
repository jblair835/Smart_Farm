"""Data Agent module.

Provides agronomic data retrieval and calculations for crop yield, evapotranspiration,
crop coefficients, and soil moisture trends.
"""

from agents.tools.usda_api import analyze_crop_yield
from agents.tools.world_bank import get_world_bank_indicator

class DataAgent:
    """
    Provides agronomic data:
    - USDA yield (optional)
    - World Bank land/ag indicators
    - ET0 (evapotranspiration)
    - Crop coefficient (Kc)
    - Estimated soil moisture trend
    """

    def run(self, crop, weather=None, growth_stage="flowering", initial_moisture=50):
        """Run data retrieval and simple agronomic calculations.

        Args:
            crop: Crop name (str).
            weather: Optional dict with keys 'temp_c' and 'wind_kmh'.
            growth_stage: Growth stage for crop coefficient lookup.
            initial_moisture: Starting soil moisture percentage.
        """

        # normalize weather inputs
        if weather is None:
            weather = {"temp_c": 25, "wind_kmh": 12}
        temp_c = weather.get("temp_c", 25)
        wind_kmh = weather.get("wind_kmh", 12)

        # 1. USDA yield data
        usda_raw = analyze_crop_yield(crop)

        # 2. World Bank data
        world_bank = get_world_bank_indicator("AG.LND.AGRI.ZS")

        # 3. Crop coefficients
        kc_values = {
            "TOMATOES": {
                "vegetative": 0.6,
                "flowering": 1.15,
                "fruiting": 1.2
            }
        }

        # 4. Calculate ET0 and Crop ET (ETc)
        et0 = self.estimate_et0(temp_c, wind_kmh)
        crop_upper = crop.upper()
        kc = kc_values.get(crop_upper, {}).get(growth_stage, 1.0)
        etc = round(et0 * kc, 2)

        # 5. Estimate soil moisture trend
        estimated_moisture = max(0, round(initial_moisture - etc, 2))
        trend = "decreasing" if etc > 0 else "stable"

        return {
            "usda_raw": usda_raw,
            "world_bank": world_bank,
            "kc_values": kc_values,
            "evapotranspiration": {
                "et0_mm_day": et0,
                "kc": kc,
                "etc_mm_day": etc
            },
            "soil_moisture_trend": {
                "initial_pct": initial_moisture,
                "estimated_next_pct": estimated_moisture,
                "trend": trend
            }
        }

    def estimate_et0(self, temp_c, wind_kmh):
        """Simple FAO Penman-Monteith approximation."""
        return round((0.408 * temp_c + 0.5 * (wind_kmh / 10)), 2)

    def speak(self, usda_raw, world_bank, moisture_trend):
        """Generate a short human-readable summary of data results.

        Args:
            usda_raw: Raw USDA yield data (any serializable type).
            world_bank: World Bank indicator result (any serializable type).
            moisture_trend: Dict with keys 'trend' and 'estimated_next_pct'.

        Returns:
            A concise string summary.
        """
        return (
            f"Millie crunching numbers — USDA: {usda_raw}, "
            f"WB: {world_bank}. "
            f"Soil moisture is expected to be {moisture_trend['trend']} "
            f"down to {moisture_trend['estimated_next_pct']}%."
        )
