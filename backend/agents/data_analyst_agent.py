"""Data Analyst Agent that creates a final company report."""

import json
from typing import Dict, List, Optional
import time

import openai

from ..utils.logger import logger

client = openai.OpenAI()

from ..tools import brave_news


def make_prompt(
    scrape_data: Dict[str, str],
    linkedin_data: Dict[str, object],
    news_data: Dict[str, object],
    extra_search: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Construct the Data Analyst Agent prompt."""
    return (
        "You are a senior sales intelligence analyst for the InsightChain platform. "
        "You will receive two JSON objects with information about a target company:\n"
        "- Scraper Output: Main company info from the website (company name, summary, sector, products/services, sales signals).\n"
        "- LinkedIn Output: Company LinkedIn profile data (LinkedIn URL, size, industry, key contacts with name/title, LinkedIn sales signals).\n"
        "\n"
        "In addition, you have access to a 'newsfinder' tool (using BraveAPI) that lets you search the web for recent news about the company. "
        "Use this tool to gather any important, recent updates or signals relevant to sales (such as funding rounds, expansions, leadership changes, awards, or problems).\n"
        "\n"
        "Your job: Synthesize all this data into a concise, practical, and actionable summary for a sales team. "
        "Focus on insights that would help a sales rep decide how, why, and to whom to reach out. "
        "Highlight decision-makers, sales opportunities, recent developments, and anything that could impact a sales pitch. "
        "Include information on production technology, machinery used, services offered, and R&D activities whenever available.\n"
        "\n"
        "Output only valid JSON using this format:\n"
        "{\n"
        '  "company_summary": "",\n'
        '  "sector": "",\n'
        '  "products_services": "",\n'
        '  "production_technology": "",\n'
        '  "machinery": "",\n'
        '  "services": "",\n'
        '  "r_and_d": "",\n'
        '  "decision_makers": [\n'
        '    {"full_name": "", "title": "", "summary": ""}\n'
        "  ],\n"
        '  "linkedin_url": "",\n'
        '  "company_size": "",\n'
        '  "location": "",\n'
        '  "sales_signals": ["", ""],\n'
        '  "recent_news": ["", ""],\n'
        '  "risks": "",\n'
        '  "actionable_insights": ["", ""]\n'
        "}\n"
        "\n"
        "If any field is unknown, leave it blank or as an empty list. Never invent or hallucinate information.\n"
        "\n"
        f"Scraper Output (JSON): {json.dumps(scrape_data)[:1000]}\n"
        f"LinkedIn Output (JSON): {json.dumps(linkedin_data)[:1000]}\n"
        f"News (JSON): {json.dumps(news_data)[:1000]}\n"
        f"Extra Search Results (JSON): {json.dumps(extra_search or [])[:1000]}"
    )


def analyze_data(
    scrape_data: Dict[str, str],
    linkedin_data: Dict[str, object],
    query: str,
    extra_search: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:
    """Run the Data Analyst agent and return final summary."""
    step = "LLM3-DataAnalystAgent"
    start = time.perf_counter()
    try:
        news_data = brave_news(query)
    except Exception:
        news_data = {"news": []}

    prompt = make_prompt(scrape_data, linkedin_data, news_data, extra_search)
    logger.info("%s INPUT: %s", step, prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        summary = response.choices[0].message.content
        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("%s OUTPUT (%d ms): %s", step, duration_ms, summary)
        try:
            data = json.loads(summary)
        except json.JSONDecodeError:
            data = {}
        # Only use decision makers provided by the LinkedIn agent
        data["decision_makers"] = linkedin_data.get("contacts", [])
        summary = json.dumps(data, ensure_ascii=False)
        return {"summary": summary, "news": news_data.get("news", []), "duration_ms": duration_ms}
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
