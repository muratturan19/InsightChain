"""LinkedIn company finder agent powered by GPT-4."""

import json
from typing import Dict

import openai

from ..utils.logger import logger

client = openai.OpenAI()

from ..tools import linkedinfinder, linkedincontacts


def make_prompt(company: str, want_contacts: bool) -> str:
    """Construct the orchestration prompt for GPT-4."""
    return (
        "You are an orchestration agent for the InsightChain platform.\n"
        "Your goal is:\n"
        "Given a company name or website, find the most accurate LinkedIn company profile URL.\n"
        "You have access to these tools:\n"
        "- linkedinfinder: Finds the correct LinkedIn company page URL from a company name or web address, using web search APIs (Exa, SerpAPI, Brave, Google CSE).\n"
        "- linkedincontacts: (Optional) Given a LinkedIn company page, extract publicly visible key employees and their positions (uses Playwright scraping).\n\n"
        "Respond in this JSON format:\n"
        "{\n"
        "  \"selected_tool\": \"linkedinfinder\",\n"
        "  \"parameters\": {\n"
        f"    \"company_name\": \"{company}\"\n"
        "  }\n"
        "}\n"
    )


def call_gpt4(prompt: str) -> Dict[str, str]:
    """Call the OpenAI API and return parsed JSON.

    Similar to the scraping agent, GPT-4 might not always return a clean JSON
    payload. We attempt to parse the content and provide a helpful error if it
    fails.
    """
    step = "LLM2-LinkedInAgent"
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


def orchestrate_linkedin(company: str, contacts: bool = False) -> Dict[str, object]:
    """Main entrypoint that orchestrates LinkedIn finding (and optionally contacts)."""
    step = "LinkedInAgent"
    logger.info("%s INPUT: %s", step, company)
    try:
        prompt = make_prompt(company, contacts)
        decision = call_gpt4(prompt)
        tool_name = decision["selected_tool"]
        params = decision.get("parameters", {})

        tools_map = {"linkedinfinder": linkedinfinder}
        if contacts:
            tools_map["linkedincontacts"] = linkedincontacts

        tool = tools_map.get(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool selected: {tool_name}")

        result = tool(**params)
        if contacts and result.get("linkedin_url"):
            result.update(linkedincontacts(result["linkedin_url"]))
        logger.info("%s OUTPUT: %s", step, result)
        return result
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
