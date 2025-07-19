"""Örnek orchestrator workflow."""

from . import agents


def run(keyword: str) -> dict:
    """Example workflow that uses the Search agent."""
    results = agents.search_agent.run_search([keyword])
    return {"keyword": keyword, "results": results}
