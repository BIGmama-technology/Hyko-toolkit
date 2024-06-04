from hyko_sdk.components.components import Ext, StorageSelect, VideoPreview
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="Video",
    task="inputs",
    description="Upload video.",
    category=Category.IO,
    icon="video",
    cost=0,
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


output_node = ToolkitNode(
    name="Video",
    task="outputs",
    description="Upload video.",
    category=Category.IO,
    icon="video",
    cost=0,
)


@output_node.set_input
class Input(CoreModel):
    output_video: Video = field(
        description="Uploaded video",
        component=VideoPreview(),
    )
