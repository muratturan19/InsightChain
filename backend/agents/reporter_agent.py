"""Reporter agent that turns analysis JSON into a polished sales report."""

from __future__ import annotations

import json
from typing import Dict, Any

import openai

from ..utils.logger import logger

client = openai.OpenAI()


REPORT_PROMPT = """
You are an expert sales analyst for Delta Proje, tasked with generating a client-facing report based strictly on structured data from previous analysis.
DO NOT HALLUCINATE or fabricate any data.
If a field is missing, clearly state "Information not available."

Your report should be concise, visually appealing, and suitable for direct sharing with sales teams or clients.
Use clear headlines, bullet points, and strong section formatting.

Report sections:

Company Overview:
Brief summary (from input)
Location, sector, company size

Key Decision Makers:
Names, titles, and short LinkedIn summaries

Growth & Sales Signals:
Any recent expansion, hiring, or other signals

Delta Proje Sales Opportunities:
Based on the company's sector and current state, which Delta Proje solutions might fit best?
Focus on:
Hydraulic Systems
Pneumatic Systems
Process Automation
AI & Digital Transformation
Make suggestions only if justified by the input data.

Actionable Recommendations:
Who to approach, with what value proposition
Potential entry points or partnership opportunities

Recent News:
List with links if available

Risks & Open Questions:
Gaps in data, ambiguities, or competitive risks

Use only information from the provided JSON input.
Do not make up numbers, projects, or contacts.
Highlight missing or unclear data directly in the report.
Output pure HTML suitable for end users.
"""


def make_prompt(analysis: Dict[str, Any]) -> str:
    """Create Reporter prompt given analysis JSON."""
    return f"{REPORT_PROMPT}\nInput JSON:\n{json.dumps(analysis, ensure_ascii=False)}"



def generate_report(analysis_json: str) -> str:
    """Generate final HTML report from analysis JSON string."""
    step = "LLM4-Reporter"
    try:
        analysis: Dict[str, Any] = json.loads(analysis_json)
    except json.JSONDecodeError:
        logger.exception("%s JSON parse error", step)
        analysis = {}

    prompt = make_prompt(analysis)
    logger.info("%s INPUT: %s", step, prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.2,
        )
        report = response.choices[0].message.content or ""
        logger.info("%s OUTPUT: %s", step, report)
        return report
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
