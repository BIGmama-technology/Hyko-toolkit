from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import PDF
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Convert Markdown content to PDF format.",
)


@func.set_input
class Inputs(CoreModel):
    markdown_string: str = Field(..., description="The Markdown content to convert.")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = Field(..., description="PDF File .")
