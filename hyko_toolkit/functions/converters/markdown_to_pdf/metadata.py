from hyko_sdk.components.components import TextField
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import Toolkit

func = Toolkit(
    category=Category.FUNCTION,
    name="markdown_to_pdf",
    task="converters",
    cost=3,
    description="Convert Markdown content to PDF format.",
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
