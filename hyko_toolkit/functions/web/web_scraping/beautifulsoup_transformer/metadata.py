from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.models import CoreModel

func = SDKFunction(
    description="Scrape HTML content from URLs and convert it to plain text"
)


@func.set_input
class Inputs(CoreModel):
    urls: list[str] = Field(
        ...,
        description="A list of URLs to scrape. Protocol must be either 'http' or 'https'.",
    )


@func.set_param
class Params(CoreModel):
    tags_to_extract: str = Field(
        ...,
        description="Specify HTML tags for extraction, separated by commas.",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(
        ..., description="List of transformed documents as plain text."
    )
