"""Data Agent module.

Provides agronomic data retrieval and calculations for crop yield, evapotranspiration,
crop coefficients, and soil moisture trends.
"""

from agents.tools.usda_api import analyze_crop_yield
from agents.tools.world_bank import get_world_bank_indicator  # Fixed import

class DataAgent:
    """
    Provides agronomic data:
    - USDA yield (optional)
    - World Bank land/ag indicators
    - ET0 (evapotranspiration)
    - Crop coefficient (Kc)
    - Estimated soil moisture trend
    """

    def run(self, crop, env=None):
        """Retrieve agronomic data and estimate crop water balance.

        Args:
            crop: Crop name string.
            env: Optional environment settings dict with keys:
                temp_c, wind_kmh, growth_stage, initial_moisture.
        """
        env = env or {}
        temp_c = env.get("temp_c", 25)
        wind_kmh = env.get("wind_kmh", 12)
        growth_stage = env.get("growth_stage", "flowering")
        initial_moisture = env.get("initial_moisture", 50)

        # 1. USDA yield data
        usda_raw = analyze_crop_yield(crop)

        # 2. World Bank data (Fixed function name)
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
        # ETc = Water lost by the plant per day (in mm)
        etc = round(et0 * kc, 2)

        # 5. Estimate soil moisture trend (Simple depletion model)
        # If no rain/irrigation occurs, moisture drops by the ETc amount
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
        """Generate a summary statement about agronomic data and moisture trends."""
        return (
            f"Millie crunching numbers — USDA: {usda_raw}, "
            f"WB: {world_bank}. "
            f"Soil moisture is expected to be {moisture_trend['trend']} "
            f"down to {moisture_trend['estimated_next_pct']}%."
        )
