from typing import Dict, List

from .linkedin_finder import linkedinfinder
from .news_search import brave_news
from .search_tools import bing_search, google_search, duckduckgo_search


def linkedin_search(company: str) -> Dict[str, str]:
    """Wrapper around linkedinfinder."""
    return linkedinfinder(company)


def newsfinder(query: str) -> Dict[str, List[Dict[str, str]]]:
    """Fetch recent news articles about a query."""
    return brave_news(query)


def trend_fetcher(topic: str) -> Dict[str, str]:
    """Placeholder function returning trending info."""
    return {"trend": f"Güncel trend verisi ({topic})"}


def product_catalogue(query: str) -> Dict[str, str]:
    """Placeholder catalogue search for Delta Proje solutions."""
    return {"products": f"{query} için önerilen Delta Proje ürünleri"}


def web_search(query: str) -> Dict[str, List[str]]:
    """Aggregate search results from multiple engines."""
    results: List[str] = []
    results.extend(bing_search(query))
    results.extend(google_search(query))
    results.extend(duckduckgo_search(query))
    return {"results": results}
