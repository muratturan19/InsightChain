"""Temel Search Agent.
Bu ajan verilen anahtar kelimeler için örnek veri döner."""

from typing import List

from ..tools import (
    bing_search,
    google_search,
    duckduckgo_search,
    company_api_search,
)


def run_search(keywords: List[str]) -> List[str]:
    """Aggregate results from multiple search tools."""
    results: List[str] = []
    for kw in keywords:
        results.extend(bing_search(kw))
        results.extend(google_search(kw))
        results.extend(duckduckgo_search(kw))
        results.extend(company_api_search(kw))
    return results
