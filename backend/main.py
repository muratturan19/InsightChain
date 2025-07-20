from fastapi import FastAPI, Query
from pydantic import BaseModel

from .agents import (
    orchestrate_scraping,
    orchestrate_linkedin,
    run_pipeline,
)

app = FastAPI(title="InsightChain API")


@app.get("/")
def read_root():
    """Basic healthcheck endpoint."""
    return {"message": "InsightChain backend is running"}


@app.get("/scrape")
def scrape(url: str = Query(..., description="Company website URL")):
    """Endpoint that triggers the scraping workflow."""
    result = orchestrate_scraping(url)
    return result


@app.get("/find_linkedin")
def find_linkedin(
    company: str = Query(..., description="Company name or website"),
    contacts: bool = Query(False, description="Also fetch public contacts"),
):
    """Endpoint that finds the LinkedIn company page (and optionally contacts)."""
    result = orchestrate_linkedin(company, contacts)
    return result


class AnalyzeRequest(BaseModel):
    website: str
    company: str | None = None


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Run the full analysis pipeline for a company website."""
    result = run_pipeline(req.website, req.company)
    return {"report": result.get("report", "")}


# Future endpoints for agent orchestration will live here.
