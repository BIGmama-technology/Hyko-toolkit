from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Pdf to text",
    icon="pdf",
    cost=3,
    description="Extracts text from pdf.",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    pdf_file: PDF = field(description="User input pdf to be converted to text")


@node.set_output
class Outputs(CoreModel):
    text: str = field(description="Extracted text from pdf")
