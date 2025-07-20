import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

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

from backend.agents.scraper_agent import crawl_site, orchestrate_scraping


class CrawlSiteTests(unittest.TestCase):
    @patch("backend.agents.scraper_agent.requests.get")
    @patch("backend.agents.scraper_agent.RobotFileParser")
    def test_collects_internal_links(self, mock_rfp_cls, mock_get):
        mock_rfp = mock_rfp_cls.return_value
        mock_rfp.read.return_value = None
        mock_rfp.can_fetch.return_value = True

        html_index = '<html><a href="/about">About</a></html>'
        html_about = '<html>About us</html>'

        def side_effect(url, timeout=10):
            resp = Mock()
            resp.raise_for_status.return_value = None
            resp.text = html_about if url.endswith("/about") else html_index
            return resp

        mock_get.side_effect = side_effect

        result = crawl_site("http://example.com", depth=1)
        self.assertIn(html_index, result)
        self.assertIn(html_about, result)
        self.assertEqual(mock_get.call_count, 2)

    @patch("backend.agents.scraper_agent.requests.get")
    @patch("backend.agents.scraper_agent.RobotFileParser")
    def test_depth_limit(self, mock_rfp_cls, mock_get):
        mock_rfp = mock_rfp_cls.return_value
        mock_rfp.read.return_value = None
        mock_rfp.can_fetch.return_value = True

        html_index = '<html><a href="/a">A</a></html>'
        html_a = '<html><a href="/b">B</a></html>'
        html_b = '<html>Deep</html>'

        def side_effect(url, timeout=10):
            resp = Mock()
            resp.raise_for_status.return_value = None
            if url.endswith('/b'):
                resp.text = html_b
            elif url.endswith('/a'):
                resp.text = html_a
            else:
                resp.text = html_index
            return resp

        mock_get.side_effect = side_effect

        result = crawl_site("http://example.com", depth=1)
        self.assertIn(html_index, result)
        self.assertIn(html_a, result)
        self.assertNotIn(html_b, result)
        self.assertEqual(mock_get.call_count, 2)


class OrchestrateScrapingTests(unittest.TestCase):
    @patch("backend.agents.scraper_agent.extract_company_info", return_value={})
    @patch("backend.agents.scraper_agent.crawl_site", return_value="<html>extra</html>")
    @patch("backend.agents.scraper_agent.scraping_tools.llmscraper", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.masscrawler", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.formbot", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.jsrender", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.staticscraper")
    def test_depth_invokes_crawler(
        self,
        mock_static,
        mock_js,
        mock_formbot,
        mock_mass,
        mock_llm,
        mock_crawl,
        mock_extract,
    ):
        mock_static.return_value = {"html": "<html>main</html>"}

        result = orchestrate_scraping("http://example.com", depth_limit=1)

        mock_crawl.assert_called_once_with("http://example.com", 1)
        self.assertIn("extra", result["html"])

    @patch("backend.agents.scraper_agent.extract_company_info", return_value={})
    @patch("backend.agents.scraper_agent.crawl_site")
    @patch("backend.agents.scraper_agent.scraping_tools.llmscraper", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.masscrawler", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.formbot", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.jsrender", return_value={"html": ""})
    @patch("backend.agents.scraper_agent.scraping_tools.staticscraper")
    def test_depth_zero_skips_crawler(
        self,
        mock_static,
        mock_js,
        mock_formbot,
        mock_mass,
        mock_llm,
        mock_crawl,
        mock_extract,
    ):
        mock_static.return_value = {"html": "<html>main</html>"}

        orchestrate_scraping("http://example.com", depth_limit=0)

        mock_crawl.assert_not_called()


if __name__ == "__main__":
    unittest.main()
