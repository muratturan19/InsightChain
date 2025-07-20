"""LinkedIn company finder agent powered by GPT-4."""

import json
from typing import Dict

import openai

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
    """Call the OpenAI API and return parsed JSON."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    content = response.choices[0].message.content
    return json.loads(content)


def orchestrate_linkedin(company: str, contacts: bool = False) -> Dict[str, object]:
    """Main entrypoint that orchestrates LinkedIn finding (and optionally contacts)."""
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
    return result
