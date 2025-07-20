
"""Backend package initialization."""

from dotenv import load_dotenv, find_dotenv

# Load environment variables from a `.env` file if present. This searches up the
# directory tree starting from the current working directory, allowing the file
# to reside in the project root.
load_dotenv(find_dotenv())
