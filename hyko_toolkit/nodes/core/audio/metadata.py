from hyko_sdk.components.components import AudioPreview, Ext, StorageSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="Audio input",
    description="Upload audio.",
    icon="audio",
    is_input=True,
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
    name="Audio output",
    description="Upload audio.",
    icon="audio",
    is_output=True,
)


@output_node.set_input
class Input(CoreModel):
    output_audio: Audio = field(
        description="Uploaded audio",
        component=AudioPreview(),
    )
