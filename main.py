import asyncio
from crawlers.bbc_crawler import BBCCrawler
from processors.article_processor import ArticleProcessor
import json
import os

os.makedirs("data/processed", exist_ok=True)


async def main():
    # Step 1: Crawl
    crawler = BBCCrawler()
    articles = await crawler.run(limit=5)

    # Step 2: Process with LangChain
    processor = ArticleProcessor()
    processed_articles = []

    for article in articles:
        result = processor.process_article(article)
        processed_articles.append(result)

    # Step 3: Save Output
    with open("data/processed/articles.json", "w", encoding="utf-8") as f:
        json.dump(processed_articles, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(processed_articles)} processed articles.")


if __name__ == "__main__":
    asyncio.run(main())
