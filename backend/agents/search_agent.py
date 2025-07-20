"""Temel Search Agent.
Bu ajan verilen anahtar kelimeler için örnek veri döner."""

from typing import List, Dict

from ..tools.search_tools import (
    serpapi_search,
    brave_search,
    google_cse_search,
)


def run_search(keywords: List[str]) -> List[Dict[str, str]]:
    """Aggregate results from multiple search tools."""
    results: List[Dict[str, str]] = []
    for kw in keywords:
        results.extend(serpapi_search(kw))
        results.extend(brave_search(kw))
        results.extend(google_cse_search(kw))
    return results
