import sys
import types
import os
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))
os.environ.setdefault("OPENAI_API_KEY", "test")

from backend.agents.reporter_agent import generate_report


class ReporterLanguageTest(unittest.TestCase):
    @patch("backend.agents.reporter_agent.client.chat.completions.create")
    def test_generate_report_returns_turkish(self, mock_create):
        msg = types.SimpleNamespace(
            content="Merhaba dünya",
            tool_calls=None,
            model_dump=lambda: {"role": "assistant", "content": "Merhaba dünya"},
        )
        mock_create.return_value = types.SimpleNamespace(choices=[types.SimpleNamespace(message=msg)])

        result = generate_report('{"company_summary": "Test", "decision_makers": []}')
        self.assertIn("Merhaba", result["html"])


if __name__ == "__main__":
    unittest.main()
