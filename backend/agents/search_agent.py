"""Temel Search Agent.
Bu ajan verilen anahtar kelimeler için örnek veri döner."""

from typing import List


def run_search(keywords: List[str]) -> List[str]:
    """Dummy search implementation."""
    # Gerçek implementasyon daha sonra eklenecek
    return [f"Result for {kw}" for kw in keywords]
