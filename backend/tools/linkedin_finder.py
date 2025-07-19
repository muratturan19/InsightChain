import os
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

EXA_API_URL = "https://api.exa.ai/search"
EXA_API_KEY = os.getenv("EXA_API_KEY")


def linkedinfinder(company_name: str) -> Dict[str, Optional[str]]:
    """Search for the most relevant LinkedIn company page URL using Exa API."""
    if not EXA_API_KEY:
        raise ValueError("EXA_API_KEY not set")

    query = f"site:linkedin.com/company {company_name}"
    payload = {"query": query, "numResults": 3}
    headers = {"Authorization": f"Bearer {EXA_API_KEY}"}
    resp = requests.post(EXA_API_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    for hit in data.get("results", []):
        url = hit.get("url", "")
        if "linkedin.com/company" in url:
            return {"linkedin_url": url}
    return {"linkedin_url": None}


def linkedincontacts(company_url: str) -> Dict[str, List[Dict[str, str]]]:
    """Extract publicly visible employee names and titles from a LinkedIn page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(company_url)
        page.wait_for_load_state("networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    employees: List[Dict[str, str]] = []
    for card in soup.select("div.org-people-profile-card__profile-info"):
        name_el = card.select_one("div>div.t-16")
        title_el = card.select_one("div>div.t-14")
        link_el = card.select_one("a.ember-view")
        if name_el and title_el and link_el:
            employees.append(
                {
                    "name": name_el.get_text(strip=True),
                    "title": title_el.get_text(strip=True),
                    "profile": "https://www.linkedin.com" + link_el.get("href"),
                }
            )
    return {"employees": employees}
