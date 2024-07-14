from hyko_sdk.components.components import (
    ComplexComponent,
    ListComponent,
    SubField,
    TextField,
    Toggle,
)
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Beautifulsoup transformer",
    cost=5,
    description="Scrape HTML content from URL.",
    # require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    url: str = field(
        description="URL to scrape. Protocol must be either 'http' or 'https'.",
        component=TextField(placeholder="Enter URL"),
    )


@node.set_param
class Params(CoreModel):
    tags_to_extract: list[str] = field(
        description="Specify HTML tags for extraction.",
        component=ListComponent(item_component=TextField(placeholder="")),
    )
    attributes_to_extract: list[dict[str, str]] = field(
        description="",
        component=ListComponent(
            item_component=ComplexComponent(
                fields=[
                    SubField(
                        type="string",
                        name="name",
                        description="description",
                        component=TextField(placeholder="Enter name"),
                    ),
                    SubField(
                        type="string",
                        name="value",
                        description="description",
                        component=TextField(placeholder="Enter value"),
                    ),
                ]
            )
        ),
    )
    strip_tags: bool = field(
        description="If true, strip HTML tags from the content.", component=Toggle()
    )


@node.set_output
class Outputs(CoreModel):
    result: str = field(description="Extracted content.")
