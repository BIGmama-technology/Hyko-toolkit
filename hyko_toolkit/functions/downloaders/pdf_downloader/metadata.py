from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="pdf_downloader",
    task="downloaders",
    description="This function downloads content from a URL and returns it as a PDF object.",
)


@func.set_input
class Inputs(CoreModel):
    url: str = Field(
        ...,
        description="Your Target PDF URL.",
    )


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = Field(..., description="The Downloaded PDF.")
