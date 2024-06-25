from hyko_sdk.components.components import Ext, ImagePreview, StorageSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="Image input",
    icon="image",
    description="Upload image.",
    is_input=True,
)


@input_node.set_output
class Output(CoreModel):
    output_image: Image = field(
        description="Uploaded image",
        component=StorageSelect(supported_ext=[Ext.PNG, Ext.JPG, Ext.JPEG]),
    )


output_node = ToolkitNode(
    name="Image output",
    icon="image",
    description="Upload image.",
    is_output=True,
)


@output_node.set_input
class Input(CoreModel):
    input_image: Image = field(
        description="Uploaded image",
        component=ImagePreview(),
    )
