from hyko_sdk.components.components import Ext, ImagePreview, StorageSelect
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="Image", task="Inputs", description="Upload image.", icon="image"
)


@input_node.set_output
class Output(CoreModel):
    output_image: Image = field(
        description="Uploaded image",
        component=StorageSelect(supported_ext=[Ext.PNG, Ext.JPG, Ext.JPEG]),
    )


output_node = ToolkitIO(
    name="Image", task="Outputs", description="Upload image.", icon="image"
)


@output_node.set_input
class Input(CoreModel):
    input_image: Image = field(
        description="Uploaded image",
        component=ImagePreview(),
    )
