from hyko_sdk.components.components import TextField
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Pdf downloader",
    task="Downloaders",
    category=Category.FUNCTION,
    name="pdf_downloader",
    task="downloaders",
    cost=2,
    description="This function downloads content from a URL and returns it as a PDF object.",
    icon="pdf",
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
