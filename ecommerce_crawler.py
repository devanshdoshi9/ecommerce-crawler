import asyncio
import json

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import deque

class EcommerceCrawler:
    def __init__(self, domains, concurrency=10):
        self.domains = domains
        self.concurrency = concurrency
        # can add any number of more patterns here to cater to new websites
        self.product_url_patterns = [
            re.compile(r"/product/", re.IGNORECASE),
            re.compile(r"/item/", re.IGNORECASE),
            re.compile(r"/p/", re.IGNORECASE),
            re.compile(r"/shop/", re.IGNORECASE)
        ]
        self.visited_urls = set()
        self.product_urls = {domain: set() for domain in domains}
        self.queue = deque()

    async def fetch(self, session: ClientSession, url: str):
        """Fetch the content of a URL."""
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
        return self.fetch(session, url)

    def is_product_url(self, url):
        """Check if a URL matches any product patterns."""
        return any(pattern.search(url) for pattern in self.product_url_patterns)

    def normalize_url(self, base_url, link):
        """Resolve a relative URL against the base URL."""
        return urljoin(base_url, link)

    async def crawl_page(self, session: ClientSession, domain: str, base_url: str):
        while len(self.queue) > 0:
            url = self.queue.popleft()

            try:
                content = await self.fetch(session, url)
                if not content:
                    return

                # parse the contents of the current page and find all the anchor tags (links) present in it
                soup = BeautifulSoup(content, "html.parser")
                for link_tag in soup.find_all("a", href=True):
                    link = self.normalize_url(base_url, link_tag["href"])

                    # skip adding a link to the queue in case its base url is different
                    parsed_url = urlparse(link)
                    if parsed_url.netloc != urlparse(base_url).netloc:
                        continue

                    # if url is not visited, we add it to the visited list and the queue
                    if link not in self.visited_urls:
                        self.visited_urls.add(link)
                        self.queue.append(link)

                # if the url matches any patterns defined above we add it to the result
                if self.is_product_url(url):
                    self.product_urls[domain].add(url)
            except Exception as e:
                print("Error occurred: ", e)

    async def crawl_domain(self, domain):
        """Crawl a single e-commerce domain."""
        async with aiohttp.ClientSession() as session:
            start_url = f"https://{domain}"
            self.queue.append(start_url)
            await self.crawl_page(session, domain, start_url)

    async def crawl_all(self):
        """Crawl all domains in parallel."""
        tasks = [self.crawl_domain(domain) for domain in self.domains]
        await asyncio.gather(*tasks)

    def run(self):
        """Run the crawler."""
        asyncio.run(self.crawl_all())
        return self.product_urls