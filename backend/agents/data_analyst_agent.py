"""Data Analyst Agent that creates a final company report."""

import json
from typing import Dict

import openai

client = openai.OpenAI()

from ..tools import brave_news


def make_prompt(
    scrape_data: Dict[str, str],
    linkedin_data: Dict[str, object],
    news_data: Dict[str, object],
) -> str:
    """Construct a prompt combining all gathered information."""
    return (
        "You are a data analyst for the InsightChain platform.\n"
        "Using the following scraped website data, LinkedIn info and recent news,\n"
        "generate a concise report about the company.\n\n"
        f"Website Data: {json.dumps(scrape_data)[:1000]}\n\n"
        f"LinkedIn Data: {json.dumps(linkedin_data)[:1000]}\n\n"
        f"News: {json.dumps(news_data)[:1000]}\n\n"
        "Return a short summary."
    )


def analyze_data(
    scrape_data: Dict[str, str], linkedin_data: Dict[str, object], query: str
) -> Dict[str, str]:
    """Run the Data Analyst agent and return final summary."""
    try:
        news_data = brave_news(query)
    except Exception:
        news_data = {"news": []}

    prompt = make_prompt(scrape_data, linkedin_data, news_data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    summary = response.choices[0].message.content
    return {"summary": summary, "news": news_data.get("news", [])}
