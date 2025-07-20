from typing import List, Dict

from .search_agent import run_search

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
    """Run enhanced search queries for given topics about the company."""
    queries: List[str] = []
    for topic in topics:
        fragments = QUERY_MAP.get(topic, [topic])
        for frag in fragments:
            queries.append(f"{company} {frag}")
    return run_search(queries)
