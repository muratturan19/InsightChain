"""Dynamic scraping agent that selects tools via GPT-4."""

import json
from typing import Dict

import openai

from ..utils.logger import logger

client = openai.OpenAI()

from ..tools import scraping_tools


def make_prompt(company_url: str) -> str:
    """Construct the decision prompt for GPT-4."""
    return (
        "You are an AI orchestration agent for the InsightChain platform.\n"
        "Your job is to select the most appropriate web scraping tool for a given company website URL based on the site's technology and scraping requirements.\n"
        "You have access to the following tools:\n"
        "- staticscraper: For simple, static HTML sites (uses requests + BeautifulSoup)\n"
        "- jsrender: For modern, JavaScript-rendered pages (uses Playwright)\n"
        "- formbot: For websites requiring form interaction or automation (uses Selenium)\n"
        "- masscrawler: For large-scale, multi-page crawling (uses Scrapy)\n"
        "- llmscraper: For AI-guided or recipe-based scraping (uses ScraperAI or similar)\n\n"
        f"Analyze the provided website (URL: {company_url}).\n"
        "Based on its content, structure, and what you can infer from the URL or any quick inspection, select the single most appropriate tool.\n\n"
        "Respond in this JSON format:\n"
        "{\n"
        "  'selected_tool': '<tool_name>',\n"
        "  'reason': '<why this tool is appropriate>',\n"
        "  'parameters': {\n"
        "    'target_url': '{company_url}'\n"
        "  }\n"
        "}\n"
    )


def call_gpt4(prompt: str) -> Dict[str, str]:
    """Call the OpenAI API and return the parsed JSON.

    The GPT-4 model occasionally returns the JSON response wrapped in text
    or fails to strictly follow the format. To make the agent more robust we
    try to extract the JSON payload and raise a clear error if parsing fails.
    """
    step = "LLM1-ScraperAgent"
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
        raise


def orchestrate_scraping(company_url: str) -> Dict[str, str]:
    """Main entrypoint for scraping orchestration."""
    step = "ScraperAgent"
    logger.info("%s INPUT: %s", step, company_url)
    try:
        prompt = make_prompt(company_url)
        decision = call_gpt4(prompt)
        selected_tool = decision["selected_tool"]
        params = decision.get("parameters", {})
        tools_map = {
            "staticscraper": scraping_tools.staticscraper,
            "jsrender": scraping_tools.jsrender,
            "formbot": scraping_tools.formbot,
            "masscrawler": scraping_tools.masscrawler,
            "llmscraper": scraping_tools.llmscraper,
        }
        tool = tools_map.get(selected_tool)
        if not tool:
            raise ValueError(f"Unknown tool selected: {selected_tool}")
        result = tool(**params)
        logger.info("%s OUTPUT: %s", step, result)
        return result
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise

