import json

from ecommerce_crawler import EcommerceCrawler


def main():
    domains = ["powerlook.in"]
    crawler = EcommerceCrawler(domains, concurrency=10)
    product_urls = crawler.run()

    for domain in domains:
        product_urls[domain] = list(product_urls[domain])

    filename = "results.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(product_urls, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()