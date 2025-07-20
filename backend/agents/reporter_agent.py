"""Reporter agent that turns analysis JSON into a polished sales report."""

from __future__ import annotations

import json
from typing import Dict, Any

import openai

from ..utils.logger import logger

client = openai.OpenAI()

# Basic CSS snippet to keep visual style consistent across reports
STYLE_SNIPPET = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400&display=swap');
body{font-family:'Open Sans',sans-serif;background:#F5F6FA;color:#003366;margin:0;padding:20px;}
h1,h2,h3{font-family:'Montserrat',sans-serif;font-weight:700;}
.card{background:#FFFFFF;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.1);padding:20px;margin-bottom:20px;}
.card h2{color:#2C85C8;font-size:24px;margin-top:0;display:flex;align-items:center;}
.alert{background:#ffe6e6;border-left:6px solid #ff0000;padding:15px;border-radius:8px;}
.actions li{margin-bottom:8px;}
.actions li::before{content:'💡';margin-right:6px;}
footer{text-align:center;margin-top:20px;color:#003366;font-size:14px;}
</style>
"""


REPORT_PROMPT = """
You are an expert sales analyst for Delta Proje. Generate a polished HTML report based
strictly on the provided analysis JSON. Never fabricate data: if something is missing,
clearly note "Bilgi yok". The report must be fully in Turkish.

Visual design requirements:
- Use Google fonts Montserrat (bold, 24px) for headings and Open Sans (16px) for text.
- Primary colors: koyu mavi #003366, açık mavi #2C85C8, vurgu #F8B400, açık gri #F5F6FA,
  beyaz #FFFFFF.
- Each section should be in a rounded "card" with subtle box-shadow and generous padding.
- Section titles may include simple icons (emoji or FontAwesome) and the title text should
  use the accent color.
- The "Riskler" section must appear in a red alert-style box.
- "Aksiyon önerileri" should be an unordered list where each item begins with a 💡 emoji.
- Finish the document with a footer: "Bu rapor Delta Proje Akıllı Satış Asistanı tarafından hazırlanmıştır.".
- Ensure a responsive layout that looks good on desktop and mobile.

Content guidelines:
- Company Overview: brief summary, location, sector and size.
- Key Decision Makers: names, titles and short LinkedIn summaries.
- Growth & Sales Signals: hiring or expansion indicators.
- Delta Proje Sales Opportunities: suggest Hydraulic, Pneumatic, Process Automation or
  AI solutions only if supported by input; otherwise state that no clear opportunity
  is visible.
- Actionable Recommendations: how to approach and what value proposition.
- Recent News: list with links if available.
- Riskler & Açık Noktalar: data gaps or competitive risks.

Output only the final HTML document – no explanations. Incorporate the required CSS
inside a <style> tag so the result can be shared as a single file."""


def make_prompt(analysis: Dict[str, Any]) -> str:
    """Create Reporter prompt given analysis JSON."""
    return (
        f"{REPORT_PROMPT}\n"
        f"Use this CSS for styling:\n{STYLE_SNIPPET}\n"
        f"Input JSON:\n{json.dumps(analysis, ensure_ascii=False)}"
    )



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
