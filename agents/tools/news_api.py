#-----------------------
# NewsAPI
#-----------------------
"""NewsAPI integration for Smart Farm project."""

from agents.tools.utils.error_handler import safe_request
from agents.tools.utils.logger import log
from agents.tools.utils.cache import cache_result

@cache_result(ttl=3600)
def get_agriculture_news(api_key="YOUR_NEWSAPI_KEY", query="agriculture"):
    """Retrieve agriculture‑related news articles from NewsAPI."""
    url = "https://newsapi.org/v2/everything"
    params = {"q": query, "apiKey": api_key}
    log(f"Fetching news articles for query '{query}'")
    return safe_request(url, params)
