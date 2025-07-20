import os
import sys
import unittest
import importlib.util
from pathlib import Path
from unittest.mock import patch

# Provide a dummy OpenAI key to avoid import errors
# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))

# Provide a dummy OpenAI key to avoid import errors
os.environ.setdefault("OPENAI_API_KEY", "test")
# Load search_tools without triggering backend.tools __init__
search_tools_path = Path(__file__).resolve().parents[1] / "tools" / "search_tools.py"
spec = importlib.util.spec_from_file_location("search_tools", search_tools_path)
search_tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_tools)

serpapi_search = search_tools.serpapi_search
google_cse_search = search_tools.google_cse_search
brave_search = search_tools.brave_search

from backend.agents.search_agent import run_search


class ToolEnvTest(unittest.TestCase):
    def test_serpapi_requires_key(self):
        env_var = os.environ.pop("SERPAPI_API_KEY", None)
        try:
            with self.assertRaises(ValueError):
                serpapi_search("OpenAI")
        finally:
            if env_var is not None:
                os.environ["SERPAPI_API_KEY"] = env_var

    def test_google_cse_requires_keys(self):
        key = os.environ.pop("GOOGLE_API_KEY", None)
        cse = os.environ.pop("GOOGLE_CSE_ID", None)
        try:
            with self.assertRaises(ValueError):
                google_cse_search("OpenAI")
        finally:
            if key is not None:
                os.environ["GOOGLE_API_KEY"] = key
            if cse is not None:
                os.environ["GOOGLE_CSE_ID"] = cse

    def test_brave_search_requires_key(self):
        key = os.environ.pop("BRAVE_API_KEY", None)
        try:
            with self.assertRaises(ValueError):
                brave_search("OpenAI")
        finally:
            if key is not None:
                os.environ["BRAVE_API_KEY"] = key


class SearchAgentTest(unittest.TestCase):
    @patch("backend.agents.search_agent.google_cse_search")
    @patch("backend.agents.search_agent.brave_search")
    @patch("backend.agents.search_agent.serpapi_search")
    def test_run_search_aggregates_results(self, mock_serpapi, mock_brave, mock_google):
        mock_serpapi.return_value = [{"title": "serp"}]
        mock_brave.return_value = [{"title": "brave"}]
        mock_google.return_value = [{"title": "google"}]

        results = run_search(["openai"])

        self.assertEqual(
            results,
            [
                {"title": "serp"},
                {"title": "brave"},
                {"title": "google"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
