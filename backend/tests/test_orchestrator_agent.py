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

from backend.agents.orchestrator_agent import run_pipeline


class PipelineDepthTest(unittest.TestCase):
    @patch("backend.agents.scraper_agent.extract_company_info", return_value={})
    @patch("backend.agents.scraper_agent.crawl_site")
    @patch("backend.agents.scraper_agent.scraping_tools.llmscraper", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.masscrawler", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.formbot", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.jsrender", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.staticscraper")
    @patch("backend.agents.orchestrator_agent.generate_report", return_value={"html": "", "duration_ms": 0})
    @patch("backend.agents.orchestrator_agent.analyze_data", return_value={"summary": "{}", "duration_ms": 0})
    @patch("backend.agents.orchestrator_agent.orchestrate_linkedin", return_value={"duration_ms": 0})
    @patch("backend.agents.orchestrator_agent.targeted_search", return_value=[])
    def test_depth_zero_skips_internal_crawl(
        self,
        mock_search,
        mock_linkedin,
        mock_analyze,
        mock_report,
        mock_static,
        mock_js,
        mock_formbot,
        mock_mass,
        mock_llm,
        mock_crawl,
        mock_extract,
    ):
        mock_static.return_value = {"html": "<html>main</html>"}

        run_pipeline("http://example.com", depth=0)

        mock_crawl.assert_not_called()


if __name__ == "__main__":
    unittest.main()
