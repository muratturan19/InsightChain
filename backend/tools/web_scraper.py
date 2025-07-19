"""Basit Web Scraper aracı (placeholder)."""

import requests


def fetch(url: str) -> str:
    """Dummy fetch function."""
    response = requests.get(url, timeout=10)
    return response.text[:200]  # sadece örnek için ilk 200 karakter
