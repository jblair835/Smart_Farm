#-----------------------
# Error Handler
#-----------------------
"""Error handling utilities for Smart Farm project."""

import requests
from agents.tools.utils.logger import log

def safe_request(url, params=None):
    """Perform a safe HTTP GET request with timeout and error handling."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        log(f"Timeout while requesting {url}")
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        log(f"Request error for {url}: {e}")
        return {"error": str(e)}
