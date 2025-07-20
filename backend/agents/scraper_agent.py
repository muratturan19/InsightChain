"""Scraper agent that sequentially tries multiple tools and extracts company info."""

import json
from typing import Dict

import openai

from ..utils.logger import logger
from ..tools import scraping_tools

client = openai.OpenAI()


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
        f"HTML:\n{html[:4000]}\n\n"
        "Respond in JSON with these keys:\n"
        "{\n"
        "  \"company_name\": \"\",\n"
        "  \"summary\": \"\",\n"
        "  \"sector\": \"\",\n"
        "  \"notable_products_or_services\": \"\",\n"
        "  \"sales_signals\": \"\"\n"
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


def orchestrate_scraping(company_url: str) -> Dict[str, str]:
    """Attempt multiple scraping tools sequentially and return extracted info."""
    step = "ScraperAgent"
    logger.info("%s INPUT: %s", step, company_url)

    tools = [
        scraping_tools.staticscraper,
        scraping_tools.jsrender,
        scraping_tools.formbot,
        scraping_tools.masscrawler,
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

    info = extract_company_info(html)
    final = {"html": html, **info}
    logger.info("%s OUTPUT: %s", step, final)
    return final
