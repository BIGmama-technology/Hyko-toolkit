from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="html2text_transformer",
    task="web_scraping",
    description="Scrape HTML content from URLs and convert it to plain text",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/web/web_scraping/html2text_transformer/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/web/web_scraping/html2text_transformer",
)


@func.set_input
class Inputs(CoreModel):
    urls: list[str] = Field(
        ...,
        description="A list of URLs to scrape. Protocol must be either 'http' or 'https'.",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(
        ..., description="List of transformed documents as plain text."
    )
