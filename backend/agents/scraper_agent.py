"""Dynamic scraping agent that selects tools via GPT-4."""

import json
from typing import Dict

import openai

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
    """Call the OpenAI API and return the parsed JSON."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    content = response.choices[0].message["content"]
    return json.loads(content)


def orchestrate_scraping(company_url: str) -> Dict[str, str]:
    """Main entrypoint for scraping orchestration."""
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
    return tool(**params)

