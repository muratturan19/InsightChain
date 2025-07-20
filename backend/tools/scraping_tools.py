"""Collection of real scraping tools used by the orchestration agent."""

from typing import Dict

import requests
from bs4 import BeautifulSoup

# Playwright imports
from playwright.sync_api import sync_playwright

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Scrapy imports
from scrapy.crawler import CrawlerProcess
from scrapy import Spider

# OpenAI for llmscraper
import openai

from ..utils.logger import logger

# create a client instance using environment variables for configuration
client = openai.OpenAI()


def staticscraper(target_url: str) -> Dict[str, str]:
    """Scrape static HTML content using requests and BeautifulSoup."""
    response = requests.get(target_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else ""
    return {"title": title, "html": response.text}


def jsrender(target_url: str) -> Dict[str, str]:
    """Render JavaScript-heavy pages using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url)
        page.wait_for_load_state("networkidle")
        content = page.content()
        browser.close()
    return {"html": content}


def formbot(target_url: str) -> Dict[str, str]:
    """Interact with pages that require automation using Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(target_url)
    html = driver.page_source
    driver.quit()
    return {"html": html}


class _SimpleSpider(Spider):
    name = "simple_spider"

    def __init__(self, url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.collected_html = ""

    def parse(self, response):
        self.collected_html = response.text


def masscrawler(target_url: str) -> Dict[str, str]:
    """Run a minimal Scrapy spider to fetch a page."""
    process = CrawlerProcess(settings={"LOG_ENABLED": False})
    spider = _SimpleSpider
    process.crawl(spider, url=target_url)
    process.start()
    html = spider.collected_html if hasattr(spider, "collected_html") else ""
    return {"html": html}


def llmscraper(target_url: str) -> Dict[str, str]:
    """Fetch page and ask OpenAI to extract key information."""
    step = "LLM-ScrapingTools.llmscraper"
    html = staticscraper(target_url)["html"]
    prompt = (
        "You are a helpful assistant that extracts key facts from webpages.\n"
        f"Content:\n{html[:4000]}\n"
        "Provide a short summary."
    )
    logger.info("%s INPUT: %s", step, prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        logger.info("%s OUTPUT: %s", step, summary)
        return {"summary": summary, "html": html}
    except Exception as exc:
        logger.exception("%s ERROR: %s", step, exc)
        raise
