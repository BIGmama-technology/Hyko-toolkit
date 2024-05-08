import json
import os
from multiprocessing import Process, Queue

import scrapy.crawler as crawler
from bs4 import BeautifulSoup
from metadata import Inputs, Outputs, Params, func
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


class CrawlerSpider(CrawlSpider):
    def __init__(
        self, start_urls: str, stop_urls: str, allowed_domains: str, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.stop_urls = stop_urls
        self.allowed_domains = allowed_domains

    name = "my_spider"
    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_xpaths=()),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        url = str(response.request.url)  # get the URL from the request
        # check if the current url is in the stop_urls list
        if url in self.stop_urls:
            raise CloseSpider(f"Stop URL found: {url}")
        html_content = "".join(
            response.xpath("//*").getall()
        )  # join html elements into a single string
        soup = BeautifulSoup(html_content, "html.parser")
        text_only = soup.get_text().replace("\n\n", "\n")
        data = {
            "url": url,
            "text": text_only,
        }
        with open("output.json", "a") as f:
            json.dump(data, f)
            f.write("\n")


def run_spider(start_urls: str, stop_urls: str, allowed_domains: str):
    def f(q):
        try:
            settings = get_project_settings()
            runner = crawler.CrawlerRunner(settings)
            deferred = runner.crawl(
                CrawlerSpider,
                start_urls=[start_urls],
                stop_urls=[stop_urls],
                allowed_domains=[allowed_domains],
            )
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if os.path.exists("output.json"):
        os.remove("output.json")
    allowed_domains = params.allowed_domains
    start_urls = inputs.start_urls
    stop_urls = inputs.stop_urls

    run_spider(start_urls, stop_urls, allowed_domains)
    with open("output.json") as f:
        output_data = [json.loads(line) for line in f]
    urls = [item["url"] for item in output_data]
    texts = [item["text"] for item in output_data]
    return Outputs(urls=urls, text=texts)
