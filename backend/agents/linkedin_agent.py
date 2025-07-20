"""LinkedIn company finder agent powered by GPT-4."""

import json
from typing import Dict

import openai

from ..utils.logger import logger

client = openai.OpenAI()




def make_prompt(company: str, want_contacts: bool) -> str:
    """Construct the LinkedIn extraction prompt for GPT-4."""
    return (
        "You are a sales intelligence agent for the InsightChain platform.\n"
        "Given a company name, your job is to help sales teams prepare for outreach by extracting the most relevant LinkedIn information about that company.\n\n"
        "Your objectives:\n"
        "- Use the given company name to find the official LinkedIn company page (not subsidiaries or similarly-named companies).\n"
        "- From that page, extract publicly available key employees\u2014especially decision-makers, executives, sales leads, and relevant managers. For each contact, provide full name, current title/role, and (if public) a short one-line summary from their LinkedIn profile.\n"
        "- If possible, note the company size, location, and industry as listed on LinkedIn.\n"
        "- If you find any recent news, growth signals, or organizational changes (leadership, funding, hiring, new markets, awards), include them as brief bullet points.\n\n"
        "Be precise and practical\u2014focus only on what will help a sales team in prospecting.\n"
        "If any information is missing, leave the field blank. Never invent or guess.\n\n"
        "Respond in JSON in this format:\n"
        "{\n"
        '  "linkedin_url": "",\n'
        '  "company_size": "",\n'
        '  "industry": "",\n'
        '  "location": "",\n'
        '  "contacts": [\n'
        '    {"full_name": "", "title": "", "summary": ""}\n'
        "  ],\n"
        '  "sales_signals": ["", ""]\n'
        "}\n"
        f"\nCompany name: {company}"
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
    """Main entrypoint that returns LinkedIn data extracted by GPT-4."""
    step = "LinkedInAgent"
    logger.info("%s INPUT: %s", step, company)
    try:
        prompt = make_prompt(company, contacts)
        linkedin_data = call_gpt4(prompt)
        logger.info("%s OUTPUT: %s", step, linkedin_data)
        return linkedin_data
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
