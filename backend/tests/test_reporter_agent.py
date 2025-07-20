import sys
import types
import os
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))
os.environ.setdefault("OPENAI_API_KEY", "test")

# Provide dummy modules for heavy scraping dependencies
sys.modules.setdefault("playwright", types.ModuleType("playwright"))
playwright_sync = types.ModuleType("playwright.sync_api")
playwright_sync.sync_playwright = lambda: None
sys.modules.setdefault("playwright.sync_api", playwright_sync)

selenium_module = types.ModuleType("selenium")
webdriver_module = types.ModuleType("selenium.webdriver")
chrome_module = types.ModuleType("selenium.webdriver.chrome")
chrome_options_module = types.ModuleType("selenium.webdriver.chrome.options")
webdriver_module.Chrome = lambda options=None: types.SimpleNamespace(get=lambda x: None, page_source="", quit=lambda: None)
chrome_options_module.Options = object
selenium_module.webdriver = webdriver_module
webdriver_module.chrome = chrome_module
chrome_module.options = chrome_options_module
sys.modules.setdefault("selenium", selenium_module)
sys.modules.setdefault("selenium.webdriver", webdriver_module)
sys.modules.setdefault("selenium.webdriver.chrome", chrome_module)
sys.modules.setdefault("selenium.webdriver.chrome.options", chrome_options_module)

scrapy_module = types.ModuleType("scrapy")
crawler_module = types.ModuleType("scrapy.crawler")
crawler_module.CrawlerProcess = object
scrapy_module.Spider = object
sys.modules.setdefault("scrapy", scrapy_module)
sys.modules.setdefault("scrapy.crawler", crawler_module)

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
