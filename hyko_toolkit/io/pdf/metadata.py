from hyko_sdk.components.components import Ext, PDFPreview, StorageSelect
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(name="PDF", task="Inputs", description="Upload pdf.", icon="pdf")


@input_node.set_output
class Output(CoreModel):
    output_pdf: PDF = field(
        description="Uploaded pdf",
        component=StorageSelect(supported_ext=[Ext.PDF]),
    )


output_node = ToolkitIO(
    name="PDF", task="Outputs", description="Upload pdf.", icon="pdf"
)


@output_node.set_input
class Input(CoreModel):
    input_pdf: PDF = field(
        description="Uploaded pdf",
        component=PDFPreview(),
    )
