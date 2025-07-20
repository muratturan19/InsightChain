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


def dispatch_tool_call(name: str, params: Dict[str, Any]) -> Any:
    """Return the tool result for the given name and params."""
    func = TOOL_DISPATCH.get(name)
    return func(params) if func else {}

client = openai.OpenAI()

# Basic CSS snippet for Delta Proje sales reports
STYLE_SNIPPET = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400&display=swap');
body{font-family:'Open Sans',sans-serif;background:#F5F6FA;color:#003366;margin:0;padding:40px 0;}
.container{max-width:850px;margin:auto;background:#fff;padding:40px 60px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.06);}
h1,h2,h3{font-family:'Montserrat',sans-serif;font-weight:700;margin-top:0;color:#003366;}
h1{font-size:32px;margin-bottom:20px;}
h2{font-size:26px;margin-bottom:12px;}
section{margin-bottom:40px;}
section+section{border-top:1px solid #E5E8EC;padding-top:30px;}
p,li{font-size:17px;line-height:1.7;}
.subtitle{color:#2C85C8;font-weight:700;}
.alert{background:#FFE6E6;border-left:6px solid #ff0000;padding:15px;}
.actions li{font-weight:bold;margin-bottom:8px;}
.actions li::before{content:'💡 ';}
footer{text-align:center;font-size:14px;color:#003366;position:fixed;bottom:0;left:0;width:100%;background:#fff;padding:8px 0;box-shadow:0 -1px 3px rgba(0,0,0,0.1);}
</style>
"""


REPORT_PROMPT = """
You are an advanced sales analyst (LLM4) working for Delta Proje.
Create a modern consulting-style HTML report using only the provided JSON analysis.
If any field is missing, explicitly note 'Bilgi yok' and never invent facts.
As Reporter Agent, you may use serpapi, BraveAPI and Google Custom Search tools
to gather up-to-date company news, milestones or decision maker changes. Chain
them logically when necessary and always cite the source with a short
reliability note. Do not hallucinate. If no information is found, explicitly say
so.

Visual design should mimic a professional business document. Use Montserrat for headings
and Open Sans for body text. The report lives inside a wide container (max 850px) with a
subtle shadow and rounded corners. Section titles are left aligned, bold and large, body
text is 17px with 1.7 line spacing. Separate sections with light gray lines (#E5E8EC) and
ample spacing. Begin with an Executive Summary section. Risks appear in a full-width light
red box with a left red border, and actionable items start with a 💡 bullet. Conclude with a
footer stating "Bu rapor Delta Proje Akıllı Satış Asistanı tarafından hazırlanmıştır.".

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
            # always append assistant message so tool replies have context
            messages.append(msg.model_dump())
            if msg.content:
                report = msg.content
                logger.info("%s OUTPUT: %s", step, report)
                return report
            for call in msg.tool_calls or []:
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                name = call.function.name
                if name == "newsfinder":
                    result = newsfinder(args.get("query", ""))
                elif name == "linkedin_search":
                    result = linkedin_search(args.get("company", ""))
                elif name == "trend_fetcher":
                    result = trend_fetcher(args.get("topic", ""))
                elif name == "product_catalogue":
                    result = product_catalogue(args.get("query", ""))
                elif name == "web_search":
                    result = web_search(args.get("query", ""))
                elif name == "serpapi_web_search":
                    result = serpapi_web_search(args.get("query", ""))
                elif name == "google_custom_search":
                    result = google_custom_search(args.get("query", ""))
                else:
                    result = {}
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result, ensure_ascii=False)})
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
