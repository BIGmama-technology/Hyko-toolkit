import json
import os
from multiprocessing import Process, Queue

from bs4 import BeautifulSoup
from metadata import Inputs, Outputs, Params, func
from scrapy.crawler import CrawlerRunner
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


class CrawlerSpider(CrawlSpider):
    # Constructor to initialize the spider with start_urls, stop_urls, and allowed_domains
    def __init__(
        self, start_urls: str, stop_urls: str, allowed_domains: str, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.stop_urls = stop_urls
        self.allowed_domains = allowed_domains

    # Spider name
    name = "my_spider"

    # Rules to follow for crawling
    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_xpaths=()),
            callback="parse_item",
            follow=True,
        ),
    )

    # Function to parse the crawled item
    def parse_item(self, response):
        # Extract URL from the response
        url = str(response.request.url)

        # Check if the current URL is in the stop_urls list
        if url in self.stop_urls:
            raise CloseSpider(f"Stop URL found: {url}")

        # Extract HTML content and convert it to text
        html_content = "".join(response.xpath("//*").getall())
        soup = BeautifulSoup(html_content, "html.parser")
        text_only = soup.get_text().replace("\n\n", "\n")

        # Construct data dictionary with URL and text content
        data = {
            "url": url,
            "text": text_only,
        }

        # Write data to output.json file
        with open("output.json", "a") as f:
            json.dump(data, f)
            f.write("\n")


def run_spider(start_urls: str, stop_urls: str, allowed_domains: str):
    # Define a function 'f' to run the spider within a separate process
    def f(q):
        try:
            # Get project settings
            settings = get_project_settings()
            # Create a CrawlerRunner instance
            runner = CrawlerRunner(settings)
            # Run the spider with the given start_urls, stop_urls, and allowed_domains
            deferred = runner.crawl(
                CrawlerSpider,
                start_urls=[start_urls],
                stop_urls=[stop_urls],
                allowed_domains=[allowed_domains],
            )
            # Add a callback to stop the Twisted reactor once the spider finishes
            deferred.addBoth(lambda _: reactor.stop())
            # Start the Twisted reactor
            reactor.run()
            # Put None in the queue to signal that the process has finished
            q.put(None)
        except Exception as e:
            # If an exception occurs, put it in the queue for the main process to handle
            q.put(e)

    # Create a queue to communicate between the main process and the spider process
    q = Queue()
    # Create a new process to run the spider
    p = Process(target=f, args=(q,))
    # Start the spider process
    p.start()
    # Wait for the spider process to finish and get the result from the queue
    result = q.get()
    # Wait for the spider process to finish completely
    p.join()

    # If an exception occurred in the spider process, raise it in the main process
    if result is not None:
        raise result


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    # Remove the existing output file if it exists
    if os.path.exists("output.json"):
        os.remove("output.json")

    # Extract parameters from inputs and params
    allowed_domains = params.allowed_domain
    start_urls = inputs.start_url
    stop_urls = inputs.stop_url

    # Run the spider to crawl web pages and extract data
    run_spider(start_urls, stop_urls, allowed_domains)

    # Read the output data from the output file
    with open("output.json") as f:
        output_data = [json.loads(line) for line in f]

    # Extract URLs and text content from the output data
    urls = [item["url"] for item in output_data]
    texts = [item["text"] for item in output_data]

    # Return the extracted URLs and text content as Outputs
    return Outputs(urls=urls, text=texts)
