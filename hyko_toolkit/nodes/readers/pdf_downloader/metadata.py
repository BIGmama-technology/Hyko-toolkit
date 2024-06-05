from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel, Tag
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Pdf downloader",
    description="This function downloads content from a URL and returns it as a PDF object.",
    icon="pdf",
    tag=Tag.readers,
    cost=2,
)


@node.set_input
class Inputs(CoreModel):
    url: str = field(
        description="Your Target PDF URL.",
        component=TextField(placeholder="Entre your URL here"),
    )


@node.set_output
class Outputs(CoreModel):
    pdf: PDF = field(description="The Downloaded PDF.")
