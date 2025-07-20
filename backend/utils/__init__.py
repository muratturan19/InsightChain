"""Utility helpers for the InsightChain backend."""

from __future__ import annotations


def normalize_url(url: str) -> str:
    """Ensure the URL has an HTTP or HTTPS scheme."""

    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url


__all__ = ["normalize_url"]

