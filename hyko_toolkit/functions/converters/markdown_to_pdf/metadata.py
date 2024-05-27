from hyko_sdk.components.components import TextField
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Markdown to pdf",
    task="Converters",
    category=Category.FUNCTION,
    cost=3,
    description="Convert Markdown content to PDF format.",
    icon="pdf",
)


@func.set_input
class Inputs(CoreModel):
    markdown_string: str = field(
        description="Markdown String",
        component=TextField(placeholder="Entre your markdown here", multiline=True),
    )


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = field(description="PDF File .")
