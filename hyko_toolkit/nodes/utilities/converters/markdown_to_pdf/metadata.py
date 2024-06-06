from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Markdown to pdf",
    cost=3,
    description="Convert Markdown content to PDF format.",
    icon="pdf",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    markdown_string: str = field(
        description="Markdown String",
        component=TextField(placeholder="Entre your markdown here", multiline=True),
    )


@node.set_output
class Outputs(CoreModel):
    pdf: PDF = field(description="PDF File .")
