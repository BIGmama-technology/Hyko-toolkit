from hyko_sdk.components.components import Ext, StorageSelect, VideoPreview
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="Video",
    task="inputs",
    description="Upload video.",
)


@input_node.set_output
class Output(CoreModel):
    output_video: Video = field(
        description="Uploaded video",
        component=StorageSelect(
            supported_ext=[
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
    name="Video",
    task="outputs",
    description="Upload video.",
)


@output_node.set_input
class Input(CoreModel):
    output_video: Video = field(
        description="Uploaded video",
        component=VideoPreview(),
    )
