"""
USDA QuickStats API helper functions with fallback logic and optional debug logging.
"""

import requests
from agents.tools.utils.cache import cache_result

USDA_BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET/"

# 🔧 Toggle debug logging here
DEBUG_USDA = False


def usda_log(message: str):
    """Print debug messages only when DEBUG_USDA is enabled."""
    if DEBUG_USDA:
        print(message)


@cache_result(ttl=86400)
def get_usda_data(
    crop: str,
    state: str = "CALIFORNIA",
    year: str = "2026",
    statistic: str = "YIELD",
    api_key: str = "",
    **extra_filters
):
    """
    Retrieve USDA QuickStats data for a given crop and filters.
    """

    params = {
        "key": api_key,
        "commodity_desc": crop.upper(),
        "state_name": state.upper(),
        "year": year,
        "statisticcat_desc": statistic.upper(),
        **extra_filters,
    }

    usda_log(f"📡 USDA Request → {params}")

    try:
        response = requests.get(USDA_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        usda_log(f"📥 USDA Response ({year}) → {len(data.get('data', []))} records")
        return data
    except (requests.RequestException, ValueError) as e:
        usda_log(f"❌ USDA API error: {e}")
        return {}


def get_usda_with_fallback(
    crop: str,
    state: str = "CALIFORNIA",
    start_year: int = 2026,
    statistic: str = "YIELD",
    api_key: str = "",
    min_year: int = 2010,
    **extra_filters
):
    """
    Try USDA QuickStats for the target year.
    If empty, fallback to earlier years until data is found.
    Logs each year attempted when debug mode is enabled.
    """

    usda_log(f"\n🔎 USDA Fallback Lookup for {crop} ({statistic}) in {state}")
    usda_log(f"   Starting at {start_year}, searching back to {min_year}...\n")

    for year in range(start_year, min_year - 1, -1):
        usda_log(f" → Trying year {year}...")

        data = get_usda_data(
            crop=crop,
            state=state,
            year=str(year),
            statistic=statistic,
            api_key=api_key,
            **extra_filters
        )

        if data and data.get("data"):
            usda_log(f" ✔ Data found for {year} (entries: {len(data['data'])})\n")
            return {
                "year_used": year,
                "results": data["data"]
            }

        usda_log(f"   No data for {year}.\n")

    usda_log(" ✖ No USDA data found in any year.\n")
    return {
        "year_used": None,
        "results": []
    }


@cache_result(ttl=86400)
def analyze_crop_yield(crop: str, **extra_filters):
    """
    Wrapper for retrieving yield data for a crop in California.
    Now uses fallback logic automatically.
    """

    return get_usda_with_fallback(
        crop=crop,
        state="CALIFORNIA",
        start_year=2026,
        statistic="YIELD",
        api_key="PnUTTijKmOyfi2EFtk78BUza9ngfVKhkjZVH24nu",
        **extra_filters
    )
