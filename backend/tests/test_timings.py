import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))

from backend.agents.linkedin_agent import orchestrate_linkedin


class DurationLoggingTest(unittest.TestCase):
    @patch("backend.agents.linkedin_agent.logger.info")
    @patch("backend.agents.linkedin_agent._search_all")
    def test_duration_logged(self, mock_search, mock_log):
        mock_search.return_value = {"serpapi": [], "brave": [], "google": []}
        orchestrate_linkedin("acme", contacts=False)
        output_call = [c for c in mock_log.call_args_list if "OUTPUT" in c.args[0]][0]
        self.assertIsInstance(output_call.args[2], int)


if __name__ == "__main__":
    unittest.main()
