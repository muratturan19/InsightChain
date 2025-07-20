"""Scraper agent that sequentially tries multiple tools and extracts company info."""

import json
from typing import Dict, List, Set, Tuple
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

import openai

from ..utils.logger import logger
from ..utils import normalize_url
from ..tools import scraping_tools

client = openai.OpenAI()


def crawl_site(start_url: str, depth: int = 1) -> str:
    """Crawl internal links under the same domain up to ``depth``.

    The crawler respects robots.txt. Network errors are logged and skipped.
    Returns the concatenated HTML of all fetched pages.
    """

    step = "ScraperAgent.crawl_site"
    start_url = normalize_url(start_url)
    parsed = urlparse(start_url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    rp = RobotFileParser()
    rp.set_url(urljoin(base, "/robots.txt"))
    try:
        rp.read()
    except Exception as exc:  # robots.txt may not exist or not be reachable
        logger.warning("%s robots.txt unavailable: %s", step, exc)
        rp = None

    visited: Set[str] = set()
    queue: List[Tuple[str, int]] = [(start_url, 0)]
    html_parts: List[str] = []

    while queue:
        url, level = queue.pop(0)
        if url in visited or level > depth:
            continue
        visited.add(url)
        path = urlparse(url).path or "/"
        if rp and not rp.can_fetch("*", path):
            logger.info("%s blocked by robots.txt: %s", step, url)
            continue
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as exc:
            logger.warning("%s failed to fetch %s: %s", step, url, exc)
            continue

        html_parts.append(resp.text)

        if level == depth:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a", href=True):
            joined = urljoin(url, link["href"])
            link_parsed = urlparse(joined)
            if link_parsed.scheme in {"http", "https"} and link_parsed.netloc == parsed.netloc:
                if joined not in visited:
                    queue.append((joined, level + 1))

    return "\n".join(html_parts)


def extract_company_info(html: str) -> Dict[str, str]:
    """Use GPT-4 to extract company info for sales preparation.

    Returns a dict with keys 'company_name', 'summary', 'sector',
    'notable_products_or_services' and 'sales_signals'.
    """
    step = "LLM1-ExtractCompany"
    prompt = (
        "You are a sales intelligence assistant for the InsightChain platform. "
        "Given the HTML of a company's website, your job is to extract key information "
        "that will help sales teams quickly understand the company and prepare for outreach.\n\n"
        "Your main goals:\n"
        "- Extract the official company name (brand, legal or most commonly used form)\n"
        "- Write a concise one-sentence summary of what the company does, focusing on its main business and any unique value proposition.\n"
        "- If possible, identify the primary industry/sector and notable products, services, or technologies.\n"
        "- Note any signals that might help a sales team (e.g. recent news, growth, awards, leadership changes, market focus, new locations, partnerships, etc.)\n\n"
        "Be brief, practical and directly useful for sales preparation. If any information is missing, just leave the field blank—do not hallucinate or make up facts.\n\n"
        # Send a larger chunk of the crawled HTML to the LLM so more context is
        # available when extracting company information.
        # 20k characters keeps the prompt size reasonable while covering most
        # landing pages.
        f"HTML:\n{html[:20000]}\n\n"
        "Respond in JSON with these keys:\n"
        "{\n"
        '  "company_name": "",\n'
        '  "summary": "",\n'
        '  "sector": "",\n'
        '  "notable_products_or_services": "",\n'
        '  "sales_signals": ""\n'
        "}"
    )
    logger.info("%s INPUT: %s", step, prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content or ""
        logger.info("%s OUTPUT: %s", step, content)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            import re

            match = re.search(r"{.*}", content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Invalid JSON from GPT-4: {content}")
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        return {
            "company_name": "",
            "summary": "",
            "sector": "",
            "notable_products_or_services": "",
            "sales_signals": "",
        }


def orchestrate_scraping(company_url: str, depth_limit: int = 0) -> Dict[str, str]:
    """Attempt multiple scraping tools sequentially and crawl internal pages.

    ``depth_limit`` controls how deep the internal crawler should go. ``0``
    disables crawling and only fetches the main page.
    """
    step = "ScraperAgent"
    company_url = normalize_url(company_url)
    logger.info("%s INPUT: %s", step, company_url)
    start = time.perf_counter()

    tools = [
        scraping_tools.staticscraper,
        scraping_tools.jsrender,
        scraping_tools.formbot,
        scraping_tools.masscrawler,
        scraping_tools.llmscraper,
    ]
    html = ""
    for tool in tools:
        try:
            result = tool(target_url=company_url)
            html = result.get("html", "")
            if html:
                break
        except Exception as exc:
            logger.exception("%s %s failed: %s", step, tool.__name__, exc)
    if not html:
        raise RuntimeError("All scraping tools failed")

    if depth_limit > 0:
        try:
            crawl_html = crawl_site(company_url, depth_limit)
            if crawl_html:
                html = f"{html}\n{crawl_html}"
        except Exception as exc:
            logger.warning("%s crawl_site failed: %s", step, exc)

    info = extract_company_info(html)
    duration_ms = int((time.perf_counter() - start) * 1000)
    final = {"html": html, **info, "duration_ms": duration_ms}
    logger.info("%s OUTPUT (%d ms): %s", step, duration_ms, final)
    return final
