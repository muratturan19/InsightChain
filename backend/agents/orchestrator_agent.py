"""Orchestrator agent that runs the full company analysis pipeline."""

from typing import Dict, Optional
import json
import time

from .scraper_agent import orchestrate_scraping
from .linkedin_agent import orchestrate_linkedin
from .data_analyst_agent import analyze_data
from .enhanced_search_agent import targeted_search
from .reporter_agent import generate_report
from ..utils.logger import logger


def run_pipeline(
    company_url: str, company_name: Optional[str] = None
) -> Dict[str, object]:
    """Run scraping, LinkedIn enrichment and final analysis."""
    step = "Pipeline"
    logger.info("%s START: %s %s", step, company_url, company_name)
    start = time.perf_counter()
    try:
        scrape_result = orchestrate_scraping(company_url)
        if not company_name:
            company_name = scrape_result.get("company_name", company_url)
        linkedin_result = orchestrate_linkedin(company_name, contacts=True)
        analysis_result = analyze_data(scrape_result, linkedin_result, company_name)

        # Check for missing fields and retry with enhanced search if needed
        max_retries = 3
        retries = 0
        while True:
            try:
                summary_data = json.loads(analysis_result.get("summary", "{}"))
            except json.JSONDecodeError:
                summary_data = {}
            missing = [
                field
                for field in [
                    "foundation",
                    "production_capacity",
                    "r_and_d",
                    "references",
                    "decision_makers",
                    "growth_signals",
                ]
                if not summary_data.get(field)
            ]
            if not missing or retries >= max_retries:
                break
            iter_start = time.perf_counter()
            search_results = targeted_search(company_name, missing)
            analysis_result = analyze_data(
                scrape_result,
                linkedin_result,
                company_name,
                search_results,
            )
            duration = time.perf_counter() - iter_start
            logger.info(
                "%s RETRY %s duration %.2fs", step, retries + 1, duration
            )
            retries += 1

        report_result = generate_report(analysis_result.get("summary", "{}"), tool_mode=True)
        duration_ms = int((time.perf_counter() - start) * 1000)
        result = {
            "scrape": scrape_result,
            "linkedin": linkedin_result,
            "analysis": analysis_result,
            "report": report_result.get("html", ""),
            "timings": {
                "scrape": scrape_result.get("duration_ms"),
                "linkedin": linkedin_result.get("duration_ms"),
                "analysis": analysis_result.get("duration_ms"),
                "report": report_result.get("duration_ms"),
                "pipeline": duration_ms,
            },
        }
        logger.info("%s OUTPUT (%d ms): %s", step, duration_ms, result)
        return result
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
