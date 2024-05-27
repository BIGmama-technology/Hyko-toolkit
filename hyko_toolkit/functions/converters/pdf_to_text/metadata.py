from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.FUNCTION,
    name="pdf_to_text",
    task="converters",
    cost=3,
    description="Extracts text from pdf.",
)


@func.set_input
class Inputs(CoreModel):
    pdf_file: PDF = field(description="User input pdf to be converted to text")


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="Extracted text from pdf")
