from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import PDF
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
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
