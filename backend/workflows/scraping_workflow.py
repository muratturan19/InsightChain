"""Workflow that triggers the scraper agent based on a URL."""

from ..agents import orchestrate_scraping


def run(url: str) -> dict:
    """Run the dynamic scraping workflow."""
    result = orchestrate_scraping(url)
    return result
