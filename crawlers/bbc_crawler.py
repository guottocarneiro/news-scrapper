import asyncio
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode


class BBCCrawler:
    def __init__(self, base_url="https://www.cnnbrasil.com.br"):
        self.base_url = base_url
        self.browser_config = BrowserConfig(headless=True)
        self.run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    async def extract_article_links(self, section="/"):
        url = self.base_url + section
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url=url, config=self.run_config)
            if result.success:
                soup = BeautifulSoup(result.html, "html.parser")
                links = set()
                test = soup.find_all("a", href=True)
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag["href"]
                    if (
                        href.__contains__("/politica/")
                        and not href.endswith("/politica/")
                        and not href.endswith(".jpg")
                    ):
                        links.add(href)
                return list(links)
            else:
                print(f"Erro ao acessar {url}: {result.error_message}")
                return []

    async def scrape_article(self, url):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url=url, config=self.run_config)
            if result.success:
                soup = BeautifulSoup(result.html, "html.parser")
                title_tag = soup.find("h1")
                title = title_tag.get_text(strip=True) if title_tag else "Sem título"
                paragraphs = soup.find_all("p")
                content = " ".join(p.get_text(strip=True) for p in paragraphs)
                return {"url": url, "title": title, "content": content}
            else:
                print(f"Erro ao acessar {url}: {result.error_message}")
                return None

    async def run(self, limit=5):
        links = await self.extract_article_links()
        articles = []
        for url in links[:limit]:
            article = await self.scrape_article(url)
            if article:
                articles.append(article)
                print(f"Artigo coletado: {article['title']}")
                return articles
