from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="html2text_transformer",
    task="web_scraping",
    description="Scrape HTML content from URLs and convert it to plain text",
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
