from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="scrapy_crawler",
    task="web_scraping",
    description="use scrapy to crawl web pages",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/web/web_scraping/scrapy_crawler/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/web/web_scraping/scrapy_crawler",
)


@func.set_input
class Inputs(CoreModel):
    start_url: str = Field(
        ...,
        description="A starting url to crawl. Protocol must be either 'http' or 'https'.",
    )
    stop_url: str = Field(
        ...,
        description="A list of urls to stop crawling. Protocol must be either 'http' or 'https'.",
    )


@func.set_param
class Params(CoreModel):
    allowed_domain: str = Field(..., description="A domain to crawl.")


@func.set_output
class Outputs(CoreModel):
    urls: list[str] = Field(..., description="A list of crawled urls.")
    text: list[str] = Field(..., description="A list of crawled text.")
