#-----------------------
# World Bank
#-----------------------
"""World Bank API integration for Smart Farm project."""

from agents.tools.utils.error_handler import safe_request
from agents.tools.utils.logger import log
from agents.tools.utils.cache import cache_result

@cache_result(ttl=86400)
def get_world_bank_indicator(indicator, country="USA"):
    """Fetch agricultural indicator data from the World Bank API."""
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    params = {"format": "json"}
    log(f"Fetching World Bank indicator {indicator} for {country}")
    data = safe_request(url, params)
    value = None
    if isinstance(data, list) and len(data) > 1 and data[1]:
        value = data[1][0].get("value")
    if value is None:
        value = "Data not available"
    return {"indicator": indicator, "value": value}
