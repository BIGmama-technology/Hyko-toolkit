from hyko_sdk.components.components import TextField
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="pdf_downloader",
    task="downloaders",
    cost=2,
    description="This function downloads content from a URL and returns it as a PDF object.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/downloaders/pdf_downloader/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/downloaders/pdf_downloader",
)


@func.set_input
class Inputs(CoreModel):
    url: str = field(
        description="Your Target PDF URL.",
        component=TextField(placeholder="Entre your URL here"),
    )


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = field(description="The Downloaded PDF.")
