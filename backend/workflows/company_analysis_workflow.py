"""Workflow that runs the full analysis pipeline."""

from ..agents import run_pipeline


def run(website: str) -> dict:
    """Run analysis pipeline for the given website."""
    return run_pipeline(website)
