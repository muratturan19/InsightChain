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

    params = {"q": query, "count": 10}
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    resp = requests.get(BRAVE_SEARCH_URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("web", {}).get("results", [])
    results: List[Dict[str, str]] = []
    for hit in items[:10]:
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

    params = {"engine": "google", "q": query, "api_key": SERPAPI_API_KEY, "num": 10}
    resp = requests.get(SERPAPI_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results: List[Dict[str, str]] = []
    for item in data.get("organic_results", [])[:10]:
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
        )
    return results


GOOGLE_API_KEYS = [k.strip() for k in os.getenv("GOOGLE_API_KEYS", "").split(",") if k.strip()]
if not GOOGLE_API_KEYS:
    single = os.getenv("GOOGLE_API_KEY")
    if single:
        GOOGLE_API_KEYS = [single]

GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"


def google_cse_search(query: str) -> List[Dict[str, str]]:
    """Search using Google Custom Search API.

    If multiple API keys are provided via ``GOOGLE_API_KEYS`` (comma separated),
    they are tried sequentially when quota errors occur.
    """
    if not GOOGLE_API_KEYS or not GOOGLE_CSE_ID:
        raise ValueError("GOOGLE_API_KEY or GOOGLE_CSE_ID not set")

    last_error = ""
    for key in GOOGLE_API_KEYS:
        params = {"key": key, "cx": GOOGLE_CSE_ID, "q": query, "num": 10}
        resp = requests.get(GOOGLE_CSE_URL, params=params, timeout=10)
        if resp.status_code == 429:
            try:
                last_error = resp.json().get("error", {}).get("message", "")
            except Exception:
                last_error = resp.text
            continue
        if resp.status_code >= 400:
            try:
                message = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                message = resp.text
            raise requests.HTTPError(message, response=resp)
        data = resp.json()
        results: List[Dict[str, str]] = []
        for item in data.get("items", [])[:10]:
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                }
            )
        return results

    raise requests.HTTPError(last_error or "Google API rate limit exceeded", response=resp)
