from typing import List, Dict

from .search_agent import run_search
from ..utils.logger import logger

# Mapping from missing field names to search query fragments
QUERY_MAP = {
    "foundation": ["foundation year", "established"],
    "production_capacity": ["production capacity"],
    "production_technology": ["production technology", "manufacturing technology"],
    "machinery": ["machinery", "equipment"],
    "services": ["services", "service offerings"],
    "r_and_d": ["R&D investment", "research and development", "innovation"],
    "references": ["customer references", "case studies"],
    "decision_makers": ["leadership team", "executives"],
    "growth_signals": ["growth signals", "investment", "expansion", "hiring"],
}


def targeted_search(company: str, topics: List[str]) -> List[Dict[str, str]]:
    """Run targeted searches for each topic using minimal API calls."""
    results: List[Dict[str, str]] = []
    seen: set[str] = set()
    for topic in topics:
        fragments = QUERY_MAP.get(topic, [topic])
        found = False
        for frag in fragments:
            query = f"{company} {frag}"
            if query in seen:
                logger.info("EnhancedSearch skip duplicate query=%s", query)
                continue
            seen.add(query)
            logger.info(
                "EnhancedSearch CALL field=%s query=%s", topic, query
            )
            res = run_search([query])
            if res:
                results.extend(res)
                found = True
                break
        if not found:
            logger.info("EnhancedSearch no result for topic=%s", topic)
    return results
