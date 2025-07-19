from fastapi import FastAPI

app = FastAPI(title="InsightChain API")


@app.get("/")
def read_root():
    """Basic healthcheck endpoint."""
    return {"message": "InsightChain backend is running"}


# Future endpoints for agent orchestration will live here.
