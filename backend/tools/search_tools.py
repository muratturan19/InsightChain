from typing import Dict, List

import os
import requests


def bing_search(query: str) -> List[str]:
    """Placeholder Bing search"""
    return [f"Bing result for {query}"]


def google_search(query: str) -> List[str]:
    """Placeholder Google search"""
    return [f"Google result for {query}"]


def duckduckgo_search(query: str) -> List[str]:
    """Placeholder DuckDuckGo search"""
    return [f"DuckDuckGo result for {query}"]


def company_api_search(query: str) -> List[str]:
    """Placeholder Company API search"""
    return [f"Company API result for {query}"]


BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"


def brave_search(query: str) -> List[Dict[str, str]]:
    """Search the web using Brave Search API."""
    if not BRAVE_API_KEY:
        raise ValueError("BRAVE_API_KEY not set")

    params = {"q": query, "count": 3}
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    resp = requests.get(BRAVE_SEARCH_URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("web", {}).get("results", [])
    results: List[Dict[str, str]] = []
    for hit in items[:3]:
        results.append(
            {
                "title": hit.get("title", ""),
                "url": hit.get("url", ""),
                "snippet": hit.get("description", ""),
            }
        )
    return results


SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
SERPAPI_URL = "https://serpapi.com/search"


def serpapi_search(query: str) -> List[Dict[str, str]]:
    """Search the web using SerpAPI and return the first few results."""
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY not set")

    params = {"engine": "google", "q": query, "api_key": SERPAPI_API_KEY, "num": 3}
    resp = requests.get(SERPAPI_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results: List[Dict[str, str]] = []
    for item in data.get("organic_results", [])[:3]:
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
        )
    return results


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"


def google_cse_search(query: str) -> List[Dict[str, str]]:
    """Search using Google Custom Search API."""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        raise ValueError("GOOGLE_API_KEY or GOOGLE_CSE_ID not set")

    params = {"key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID, "q": query}
    resp = requests.get(GOOGLE_CSE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results: List[Dict[str, str]] = []
    for item in data.get("items", [])[:3]:
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
        )
    return results
