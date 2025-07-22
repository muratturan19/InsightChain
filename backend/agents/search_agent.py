"""Temel Search Agent.
Bu ajan verilen anahtar kelimeler için örnek veri döner."""

from typing import List, Dict

from ..tools.search_tools import (
    serpapi_search,
    brave_search,
    google_cse_search,
)
from ..utils.logger import logger

TOOL_SEQUENCE = [
    "google_cse_search",
    "serpapi_search",
    "brave_search",
]

TOOL_LABELS = {
    "google_cse_search": "google_cse",
    "serpapi_search": "serpapi",
    "brave_search": "brave",
}


def run_search(keywords: List[str]) -> List[Dict[str, str]]:
    """Search each keyword using the tool sequence until results are found.

    Duplicate keyword queries are ignored within a single call.
    """
    results: List[Dict[str, str]] = []
    seen = set()
    for kw in keywords:
        if kw in seen:
            logger.info("SearchAgent skip duplicate query=%s", kw)
            continue
        seen.add(kw)
        for name in TOOL_SEQUENCE:
            func = globals()[name]
            label = TOOL_LABELS[name]
            try:
                logger.info("SearchAgent CALL tool=%s query=%s", label, kw)
                res = func(kw)
                logger.info(
                    "SearchAgent RESULT tool=%s query=%s count=%d",
                    label,
                    kw,
                    len(res),
                )
                if res:
                    results.extend(res)
                    break
            except Exception as exc:
                logger.exception(
                    "SearchAgent ERROR tool=%s query=%s: %s", label, kw, exc
                )
                continue
    return results
