"""Reporter agent that turns analysis JSON into a polished sales report."""

from __future__ import annotations

import json
from typing import Any, Dict

import openai

from ..utils.logger import logger
from ..tools import (
    linkedin_search,
    newsfinder,
    trend_fetcher,
    product_catalogue,
    web_search,
    serpapi_web_search,
    google_custom_search,
)

# Map tool names to callables for easier dispatching
TOOL_DISPATCH = {
    "newsfinder": lambda p: newsfinder(p.get("query", "")),
    "linkedin_search": lambda p: linkedin_search(p.get("company", "")),
    "trend_fetcher": lambda p: trend_fetcher(p.get("topic", "")),
    "product_catalogue": lambda p: product_catalogue(p.get("query", "")),
    "web_search": lambda p: web_search(p.get("query", "")),
    "serpapi_web_search": lambda p: serpapi_web_search(p.get("query", "")),
    "google_custom_search": lambda p: google_custom_search(p.get("query", "")),
}

client = openai.OpenAI()

# Basic CSS snippet for Delta Proje sales reports
STYLE_SNIPPET = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400&display=swap');
body{font-family:'Open Sans',sans-serif;background:#F5F6FA;color:#003366;margin:0;padding:20px;}
h1,h2,h3{font-family:'Montserrat',sans-serif;font-weight:700;}
.container{max-width:800px;margin:auto;}
.card{background:#FFFFFF;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);padding:20px;margin-bottom:20px;}
.card h2{color:#2C85C8;font-size:24px;margin-top:0;display:flex;align-items:center;}
.alert{background:#ffe6e6;border-left:6px solid #ff0000;padding:15px;border-radius:8px;}
.actions li{margin-bottom:8px;}
.actions li::before{content:'💡';margin-right:6px;}
footer{text-align:center;margin-top:20px;color:#003366;font-size:14px;}
</style>
"""


REPORT_PROMPT = """
You are an advanced sales analyst (LLM4) working for Delta Proje.
Create a modern, card-based HTML report using only the provided JSON analysis.
If any field is missing, explicitly note 'Bilgi yok' and never invent facts.
As Reporter Agent, you may use serpapi, BraveAPI and Google Custom Search tools
to gather up-to-date company news, milestones or decision maker changes. Chain
them logically when necessary and always cite the source with a short
reliability note. Do not hallucinate. If no information is found, explicitly say
so.

Visual design must follow Delta Proje guidelines: Montserrat headings, Open Sans text,
primary colors #003366 and #2C85C8 with accent #F8B400. Each section should be a rounded
card with spacing and box-shadow. Use simple emoji or FontAwesome icons. Risks appear in
a red alert box and actionable items start with a 💡 emoji. Conclude with a footer
stating "Bu rapor Delta Proje Akıllı Satış Asistanı tarafından hazırlanmıştır.".

Content to include:
- Şirket Özeti, sektör, büyüklük ve lokasyon
- Karar Vericiler (isim, unvan, kısa LinkedIn notu)
- Satış/Growth Sinyalleri
- Delta Proje Satış Fırsatları (Hydraulic, Pneumatic, Process Automation, AI)
- Aksiyon Önerileri ve Değer Önerisi
- Güncel Haberler (varsa linkli)
- Riskler ve Açık Noktalar

If tools cannot retrieve new information, write 'Son 6 ayda şirketle ilgili kayda
değer gelişme bulunamadı'. Return only a complete HTML document with embedded
CSS; no extra commentary."""


def make_prompt(analysis: Dict[str, Any]) -> str:
    """Create Reporter prompt given analysis JSON."""
    return (
        f"{REPORT_PROMPT}\n"
        f"Use this CSS for styling:\n{STYLE_SNIPPET}\n"
        f"Input JSON:\n{json.dumps(analysis, ensure_ascii=False)}"
    )


def generate_report(analysis_json: str, tool_mode: bool = False) -> str:
    """Generate final HTML report from analysis JSON string.

    If ``tool_mode`` is True, the LLM can call additional tools to enrich the
    report. The function handles the tool calling loop until the model returns
    final HTML content.
    """
    step = "LLM4-Reporter"
    try:
        analysis: Dict[str, Any] = json.loads(analysis_json)
    except json.JSONDecodeError:
        logger.exception("%s JSON parse error", step)
        analysis = {}

    prompt = make_prompt(analysis)
    logger.info("%s INPUT: %s", step, prompt)

    messages = [{"role": "user", "content": prompt}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "newsfinder",
                "description": "Find recent news articles about a query",
                "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "linkedin_search",
                "description": "Find the LinkedIn page for a company",
                "parameters": {"type": "object", "properties": {"company": {"type": "string"}}, "required": ["company"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "trend_fetcher",
                "description": "Get trend data for a topic",
                "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "product_catalogue",
                "description": "Retrieve Delta Proje product suggestions",
                "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "General web search results",
                "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "serpapi_web_search",
                "description": "Search Google via SerpAPI",
                "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "google_custom_search",
                "description": "Google Custom Search results",
                "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            },
        },
    ]

    try:
        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=1.2,
                tools=tools if tool_mode else None,
            )
            msg = response.choices[0].message
            messages.append(msg.model_dump(exclude_none=True))

            if msg.tool_calls:
                for call in msg.tool_calls:
                    try:
                        args = json.loads(call.function.arguments or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    func = TOOL_DISPATCH.get(call.function.name)
                    result = func(args) if func else {}
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": json.dumps(result, ensure_ascii=False),
                        }
                    )
                continue

            report = msg.content or ""
            logger.info("%s OUTPUT: %s", step, report)
            return report
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
