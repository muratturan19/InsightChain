import os
import sys
import types
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
