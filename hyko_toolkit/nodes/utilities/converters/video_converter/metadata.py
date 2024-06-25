from enum import Enum

from hyko_sdk.components.components import Ext
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Video converter",
    cost=3,
    description="Convert a video from one format to another.",
    icon="video",
    require_worker=True,
)


class SupportedTypes(Enum):
    webm = Ext.WEBM
    mp4 = Ext.MP4
    avi = Ext.AVI
    mkv = Ext.MKV
    mov = Ext.MOV
    wmv = Ext.WMV
    gif = Ext.GIF


@node.set_input
class Inputs(CoreModel):
    input_video: Video = field(description="Input Video.")


@node.set_param
class Params(CoreModel):
    target_type: SupportedTypes = field(description="The Target Type.")


@node.set_output
class Outputs(CoreModel):
    output_video: Video = field(description="Converted Video.")
