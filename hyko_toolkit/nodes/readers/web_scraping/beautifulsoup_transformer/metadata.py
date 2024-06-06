from hyko_sdk.components.components import ListComponent, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Beautifulsoup transformer",
    cost=5,
    description="Scrape HTML content from URLs and convert it to plain text",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    urls: list[str] = field(
        description="A list of URLs to scrape. Protocol must be either 'http' or 'https'.",
        component=ListComponent(item_component=TextField(placeholder="Enter URL")),
    )


@node.set_param
class Params(CoreModel):
    tags_to_extract: str = field(
        description="Specify HTML tags for extraction, separated by commas."
    )


@node.set_output
class Outputs(CoreModel):
    result: list[str] = field(
        description="List of transformed documents as plain text."
    )
