"""Respectful web scraper for public, authorized pages."""
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import random
import time
import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

logger = get_logger("web_scraper")

@dataclass
class ScrapeResult:
    url: str
    title: str
    text: str
    links: list

class WebScraper:
    def __init__(self, user_agents=None, proxies=None, delay_seconds=1.5,
                 timeout_seconds=15, respect_robots=True):
        self.user_agents = user_agents or ["AutomationSuite/1.0"]
        self.proxies = proxies or []
        self.delay_seconds = delay_seconds
        self.timeout_seconds = timeout_seconds
        self.respect_robots = respect_robots
        self.session = requests.Session()
        self._last_request = 0.0

    def _robots_allowed(self, url):
        if not self.respect_robots:
            return True
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            rp = RobotFileParser(robots_url)
            rp.read()
            return rp.can_fetch(self.user_agents[0], url)
        except Exception:
            # If robots.txt cannot be read, do not claim authorization; fail closed.
            logger.warning("Could not read robots.txt for %s", parsed.netloc)
            return False

    def fetch(self, url):
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        if not self._robots_allowed(url):
            raise PermissionError("robots.txt does not permit this fetch or could not be verified")

        elapsed = time.time() - self._last_request
        if elapsed < self.delay_seconds:
            time.sleep(self.delay_seconds - elapsed)

        headers = {"User-Agent": random.choice(self.user_agents)}
        proxy = random.choice(self.proxies) if self.proxies else None
        proxies = {"http": proxy, "https": proxy} if proxy else None

        response = self.session.get(
            url, headers=headers, proxies=proxies,
            timeout=self.timeout_seconds
        )
        self._last_request = time.time()
        response.raise_for_status()
        logger.info("Fetched %s (%s)", url, response.status_code)
        return response.text

    def parse(self, url, html):
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(" ", strip=True)
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        return ScrapeResult(url, title, text, links)

    def scrape(self, url, css_selector=None):
        html = self.fetch(url)
        result = self.parse(url, html)
        if css_selector:
            soup = BeautifulSoup(html, "html.parser")
            result.text = " ".join(x.get_text(" ", strip=True) for x in soup.select(css_selector))
        return result
