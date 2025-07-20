
"""Backend package initialization."""

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Load environment variables from a `.env` file if present. The search begins at
# the current working directory and continues upward so a project root `.env`
# takes precedence. If nothing is found, fall back to a `.env` located next to
# this file (i.e. inside the backend package).
dotenv_path = find_dotenv()
if not dotenv_path:
    backend_env = Path(__file__).with_name('.env')
    if backend_env.exists():
        dotenv_path = str(backend_env)

load_dotenv(dotenv_path)
