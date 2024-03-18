from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="markdown_to_pdf",
    task="converters",
    description="Convert Markdown content to PDF format.",
)


@func.set_input
class Inputs(CoreModel):
    markdown_string: str = Field(..., description="The Markdown content to convert.")


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = Field(..., description="PDF File .")
