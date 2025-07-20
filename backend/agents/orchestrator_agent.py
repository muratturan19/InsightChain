"""Orchestrator agent that runs the full company analysis pipeline."""

from typing import Dict, Optional

from .scraper_agent import orchestrate_scraping
from .linkedin_agent import orchestrate_linkedin
from .data_analyst_agent import analyze_data
from .reporter_agent import generate_report
from ..utils.logger import logger


def run_pipeline(
    company_url: str, company_name: Optional[str] = None
) -> Dict[str, object]:
    """Run scraping, LinkedIn enrichment and final analysis."""
    step = "Pipeline"
    logger.info("%s START: %s %s", step, company_url, company_name)
    try:
        scrape_result = orchestrate_scraping(company_url)
        if not company_name:
            company_name = scrape_result.get("company_name", company_url)
        linkedin_result = orchestrate_linkedin(company_name, contacts=True)
        analysis_result = analyze_data(scrape_result, linkedin_result, company_name)
        report_html = generate_report(analysis_result.get("summary", "{}"))
        result = {
            "scrape": scrape_result,
            "linkedin": linkedin_result,
            "analysis": analysis_result,
            "report": report_html,
        }
        logger.info("%s OUTPUT: %s", step, result)
        return result
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
