from fastapi import FastAPI, Query

from .agents import orchestrate_scraping

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


# Future endpoints for agent orchestration will live here.
