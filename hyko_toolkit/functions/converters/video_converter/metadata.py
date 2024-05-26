from enum import Enum

from hyko_sdk.components.components import Ext
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="Video converter",
    task="Converters",
    cost=3,
    description="Convert a video from one format to another.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/converters/video_converter/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/converters/video_converter",
    icon="video",
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
