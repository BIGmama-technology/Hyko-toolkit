from hyko_sdk.components.components import AudioPreview, Ext, StorageSelect
from hyko_sdk.io import Audio
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

input_node = ToolkitNode(
    name="Audio",
    task="inputs",
    description="Upload audio.",
    category=Category.IO,
    cost=0,
)


@input_node.set_output
class Output(CoreModel):
    output_audio: Audio = field(
        description="Uploaded audio",
        component=StorageSelect(
            supported_ext=[
                Ext.WAV,
                Ext.MP3,
                Ext.MPEG,
                Ext.WEBM,
                Ext.MP4,
                Ext.AVI,
                Ext.MKV,
                Ext.MOV,
                Ext.WMV,
            ]
        ),
    )


output_node = ToolkitNode(
    name="Audio",
    task="outputs",
    description="Upload audio.",
    category=Category.IO,
    cost=0,
)


@output_node.set_input
class Input(CoreModel):
    output_audio: Audio = field(
        description="Uploaded audio",
        component=AudioPreview(),
    )
