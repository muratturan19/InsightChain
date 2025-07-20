from fastapi import FastAPI, Query
from pydantic import BaseModel
import socket

from .agents import (
    orchestrate_scraping,
    orchestrate_linkedin,
    run_pipeline,
)

app = FastAPI(title="InsightChain API")


def check_port_443(host: str = "google.com") -> bool:
    """Return True if a TCP connection to host:443 succeeds."""
    try:
        with socket.create_connection((host, 443), timeout=3):
            return True
    except OSError:
        return False


@app.get("/check_internet")
def check_internet():
    """Check outbound HTTPS connectivity."""
    for host in ("google.com", "api.serpapi.com", "www.bing.com"):
        if check_port_443(host):
            return {"ok": True}
    return {
        "ok": False,
        "error": "İNTERNET BAĞLANTISI KURULAMADI. Lütfen bağlantınızı kontrol edin ve 443 portuna erişimin açık olduğuna emin olun",
    }


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
    depth: int = 1


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Run the full analysis pipeline for a company website."""
    result = run_pipeline(req.website, req.company, req.depth)
    return result


# Future endpoints for agent orchestration will live here.
