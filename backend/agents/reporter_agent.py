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
/* Box styling so the action and value section matches other boxes */
.actions-box{background:#F5F6FA;padding:20px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.06);}
footer{text-align:center;font-size:14px;color:#003366;position:fixed;bottom:0;left:0;width:100%;background:#fff;padding:8px 0;box-shadow:0 -1px 3px rgba(0,0,0,0.1);}
</style>
"""


REPORT_PROMPT = """
Delta Proje adına çalışan deneyimli bir satış analistisin. Verilen JSON verilerini kullanarak modern bir danışmanlık raporu üret.
Her başlıkta sektör odaklı, uygulanabilir ve özgün açıklamalar yap. Veri eksikse 'Bilgi yok' de; kesinlikle uydurma.
Karar vericiler bölümünde yalnızca Input JSON'daki `decision_makers` listesini kullan; liste boşsa "Bilgi yok" yaz ve yeni isimler uydurma.
Gerekli durumlarda serpapi, BraveAPI veya Google Custom Search ile güncel haber, yeni atama ve büyüme sinyallerini topla ve kaynağını belirt.

Rapor şu bölümlerden oluşmalı:
* Başta 2-3 cümlelik güçlü bir Executive Summary bulunmalı.
* Ardından şirket özeti, karar vericiler, büyüme ve satış sinyalleri, Delta Proje satış fırsatları, aksiyon ve değer önerileri, güncel haberler ile riskler sıralanmalı.
* "Delta Proje Satış Fırsatları" kısmında hidrolik, pnömatik, proses otomasyonu ve yapay zekâ çözümlerinin müşterinin hangi süreçlerinde katma değer yaratacağı kısa senaryolarla açıklanmalı.
* "Growth/Market Sinyalleri" bölümünde yatırım, yeni tesis veya işe alım gibi somut göstergeler varsa hikâyeleştirilmeli.
* "Aksiyon ve Değer Önerileri" bölümü, zamanlama ve teklif yaklaşımını içeren maddeleri listeler. Bu kısım `<section class='actions-box'><ul class='actions'>` yapısı kullanılarak raporun geri kalanındaki kutu formatıyla aynı stilde gösterilmeli.
* Veri yoksa "Bilgi yok" yazılmalı.

Görsel tasarım profesyonel bir iş dokümanını andırmalı. Montserrat başlık, Open Sans gövde yazısı kullan; 850px genişliğinde gölgeli ve yuvarlak köşeli konteyner tercih et. Başlıklar kalın, metin 17px ve satır aralığı 1.7 olmalı. Bölümler gri çizgiyle ayrılmalı. Riskler kırmızı kutuda gösterilmeli. Aksiyon maddeleri 💡 ikonu ile başlamalı. Raporun altında "Bu rapor Delta Proje Akıllı Satış Asistanı tarafından hazırlanmıştır." yazan bir footer bulunmalı.

Son 6 ayda kayda değer gelişme yoksa bunu açıkça belirt. Yalnızca CSS gömülü tam HTML dökümanı döndür; ek yorum yapma."""


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
