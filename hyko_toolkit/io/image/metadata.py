from hyko_sdk.components import Ext, ImagePreview, StorageSelect
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="Image",
    task="inputs",
    description="Upload image.",
)


@input_node.set_output
class Output(CoreModel):
    output_image: Image = field(
        description="Uploaded image",
        component=StorageSelect(supported_ext=[Ext.PNG, Ext.JPG, Ext.JPEG]),
    )


output_node = ToolkitIO(
    name="Image",
    task="inputs",
    description="Upload image.",
)


@output_node.set_output
class Input(CoreModel):
    input_image: Image = field(
        description="Uploaded image",
        component=ImagePreview(),
    )


print(output_node.dump_metadata())
