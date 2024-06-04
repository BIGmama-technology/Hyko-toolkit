from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Pdf to text",
    task="Converters",
    icon="pdf",
    category=Category.FUNCTION,
    cost=3,
    description="Extracts text from pdf.",
)


@func.set_input
class Inputs(CoreModel):
    pdf_file: PDF = field(description="User input pdf to be converted to text")


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="Extracted text from pdf")
