from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="pdf_to_text",
    task="converters",
    description="Extracts text from pdf.",
)


@func.set_input
class Inputs(CoreModel):
    pdf_file: PDF = Field(..., description="User input pdf to be converted to text")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    text: str = Field(..., description="Extracted text from pdf")
