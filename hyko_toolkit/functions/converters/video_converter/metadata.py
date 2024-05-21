from enum import Enum

from hyko_sdk.components.components import Ext
from hyko_sdk.io import Video
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import Toolkit

func = Toolkit(
    category=Category.FUNCTION,
    name="video_converter",
    task="converters",
    cost=3,
    description="Convert a video from one format to another.",
)


class SupportedTypes(Enum):
    webm = Ext.WEBM
    mp4 = Ext.MP4
    avi = Ext.AVI
    mkv = Ext.MKV
    mov = Ext.MOV
    wmv = Ext.WMV
    gif = Ext.GIF


@func.set_input
class Inputs(CoreModel):
    input_video: Video = field(description="Input Video.")


@func.set_param
class Params(CoreModel):
    target_type: SupportedTypes = field(description="The Target Type.")


@func.set_output
class Outputs(CoreModel):
    output_video: Video = field(description="Converted Video.")
