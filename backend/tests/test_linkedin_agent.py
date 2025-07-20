import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))
os.environ.setdefault("OPENAI_API_KEY", "test")

from backend.agents.linkedin_agent import _search_all


class SearchAllResultsTest(unittest.TestCase):
    @patch("backend.agents.linkedin_agent.google_cse_search")
    @patch("backend.agents.linkedin_agent.brave_search")
    @patch("backend.agents.linkedin_agent.serpapi_search")
    def test_returns_at_least_ten(self, mock_serpapi, mock_brave, mock_google):
        mock_serpapi.return_value = [{"url": "https://linkedin.com/1"}] * 4
        mock_brave.return_value = [{"url": "https://linkedin.com/2"}] * 4
        mock_google.return_value = [{"url": "https://linkedin.com/3"}] * 4

        results = _search_all("acme")
        total = sum(len(v) for v in results.values())
        self.assertGreaterEqual(total, 10)


if __name__ == "__main__":
    unittest.main()
