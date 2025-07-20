import os
from typing import Dict, List

import requests

BRAVE_API_URL = "https://api.search.brave.com/res/v1/news/search"
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")


def brave_news(query: str) -> Dict[str, List[Dict[str, str]]]:
    """Fetch latest news articles about the query using Brave Search API."""
    if not BRAVE_API_KEY:
        raise ValueError("BRAVE_API_KEY not set")

    params = {"q": query, "count": 3}
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    resp = requests.get(BRAVE_API_URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items: List[Dict[str, str]] = []
    for hit in data.get("results", []):
        items.append({"title": hit.get("title", ""), "url": hit.get("url", "")})
    return {"news": items}
