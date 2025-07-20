"""Orchestrator agent that runs the full company analysis pipeline."""

from typing import Dict

from .scraper_agent import orchestrate_scraping
from .linkedin_agent import orchestrate_linkedin
from .data_analyst_agent import analyze_data


def run_pipeline(company_url: str) -> Dict[str, object]:
    """Run scraping, LinkedIn enrichment and final analysis."""
    scrape_result = orchestrate_scraping(company_url)
    linkedin_result = orchestrate_linkedin(company_url, contacts=True)
    analysis_result = analyze_data(scrape_result, linkedin_result, company_url)
    return {
        "scrape": scrape_result,
        "linkedin": linkedin_result,
        "analysis": analysis_result,
    }
