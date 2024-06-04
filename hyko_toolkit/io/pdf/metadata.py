from hyko_sdk.components.components import Ext, PDFPreview, StorageSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="PDF",
    task="inputs",
    description="Upload pdf.",
    category=Category.IO,
    icon="pdf",
    cost=0,
)


@input_node.set_output
class Output(CoreModel):
    output_pdf: PDF = field(
        description="Uploaded pdf",
        component=StorageSelect(supported_ext=[Ext.PDF]),
    )


output_node = ToolkitNode(
    name="PDF",
    task="outputs",
    description="Upload pdf.",
    category=Category.IO,
    icon="pdf",
    cost=0,
)


@output_node.set_input
class Input(CoreModel):
    input_pdf: PDF = field(
        description="Uploaded pdf",
        component=PDFPreview(),
    )
