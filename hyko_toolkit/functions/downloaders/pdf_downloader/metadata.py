from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="pdf_downloader",
    task="downloaders",
    description="This function downloads content from a URL and returns it as a PDF object.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/downloaders/pdf_downloader/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/downloaders/pdf_downloader",
)


@func.set_input
class Inputs(CoreModel):
    url: str = Field(..., description="Your Target PDF URL.")


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = Field(..., description="The Downloaded PDF.")
