# agents/data_agent.py

import math
from agents.tools.usda_api import analyze_crop_yield
from agents.tools.world_bank_api import get_world_bank_data

class DataAgent:
    """
    Provides agronomic data:
    - USDA yield (optional)
    - World Bank land/ag indicators
    - ET0 (evapotranspiration)
    - Crop coefficient (Kc)
    - Estimated soil moisture trend
    """

    def run(self, crop):
        # USDA yield data
        usda_raw = analyze_crop_yield(crop)

        # World Bank fallback
        world_bank = get_world_bank_data("AG.LND.AGRI.ZS")

        # Crop coefficients (simplified)
        kc_values = {
            "TOMATOES": {
                "vegetative": 0.6,
                "flowering": 1.15,
                "fruiting": 1.2
            }
        }

        return {
            "usda_raw": usda_raw,
            "world_bank": world_bank,
            "kc_values": kc_values
        }

    def estimate_et0(self, temp_c, wind_kmh):
        """Simple FAO Penman-Monteith approximation."""
        return round((0.408 * temp_c + 0.5 * (wind_kmh / 10)), 2)

    def speak(self, usda_raw, world_bank):
        return (
            f"Millie crunching numbers — USDA: {usda_raw}, "
            f"WB: {world_bank}."
        )
