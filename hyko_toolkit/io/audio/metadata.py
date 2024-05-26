from hyko_sdk.components.components import AudioPreview, Ext, StorageSelect
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="Audio", task="Inputs", description="Upload audio.", icon="audio"
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


output_node = ToolkitIO(
    name="Audio", task="Outputs", description="Upload audio.", icon="audio"
)


@output_node.set_input
class Input(CoreModel):
    output_audio: Audio = field(
        description="Uploaded audio",
        component=AudioPreview(),
    )
