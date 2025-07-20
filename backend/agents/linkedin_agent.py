"""LinkedIn company finder agent.

Ajan asla içerik uydurmaz, sadece harici API araması sonucu veri döndürür.
"""

from typing import Dict, List
import time

from ..utils.logger import logger
from ..tools.search_tools import serpapi_search, brave_search, google_cse_search


def _parse_contact(result: Dict[str, str]) -> Dict[str, str]:
    """Return contact dict from a search result."""
    title = result.get("title", "")
    name = title.split("-")[0].split("|")[0].strip()
    role = ""
    if "-" in title:
        role = title.split("-")[1].split("|")[0].strip()
    return {
        "full_name": name,
        "title": role,
        "summary": result.get("snippet", ""),
        "source_url": result.get("url", ""),
    }


def _search_all(query: str) -> Dict[str, List[Dict[str, str]]]:
    """Run SerpAPI, Brave and Google searches sequentially."""
    results = {"serpapi": [], "brave": [], "google": []}
    try:
        results["serpapi"] = serpapi_search(query)
    except Exception as exc:
        logger.exception("serpapi_search failed: %s", exc)

    if not any("linkedin.com" in r.get("url", "") for r in results["serpapi"]):
        try:
            results["brave"] = brave_search(query)
        except Exception as exc:
            logger.exception("brave_search failed: %s", exc)

    if not any(
        "linkedin.com" in r.get("url", "") for lst in results.values() for r in lst
    ):
        try:
            results["google"] = google_cse_search(query)
        except Exception as exc:
            logger.exception("google_custom_search failed: %s", exc)

    return results


def orchestrate_linkedin(company: str, contacts: bool = False) -> Dict[str, object]:
    """Find LinkedIn info using external search engines only."""
    step = "LinkedInAgent"
    logger.info("%s INPUT: %s", step, company)
    start = time.perf_counter()

    query = f"site:linkedin.com/in OR site:linkedin.com/company {company}"
    search_results = _search_all(query)

    linkedin_url = ""
    contact_list: List[Dict[str, str]] = []

    for source_results in search_results.values():
        for res in source_results:
            url = res.get("url", "")
            if not linkedin_url and "linkedin.com/company" in url:
                linkedin_url = url
            if contacts and "linkedin.com/in" in url:
                contact_list.append(_parse_contact(res))

    note = ""
    if not linkedin_url and not contact_list:
        note = "Bilgi yok"

    result = {
        "linkedin_url": linkedin_url,
        "company_size": "",
        "industry": "",
        "location": "",
        "contacts": contact_list,
        "search_results": search_results,
        "note": note,
    }
    duration_ms = int((time.perf_counter() - start) * 1000)
    result["duration_ms"] = duration_ms
    logger.info("%s OUTPUT (%d ms): %s", step, duration_ms, result)
    return result
