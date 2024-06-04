from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Pdf downloader",
    task="Downloaders",
    category=Category.FUNCTION,
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
