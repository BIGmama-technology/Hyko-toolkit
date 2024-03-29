from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel, Ext
from pydantic import Field

func = ToolkitFunction(
    name="video_converter",
    task="converters",
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
    input_video: Video = Field(..., description="Input Video.")


@func.set_param
class Params(CoreModel):
    target_type: SupportedTypes = Field(
        ...,
        description="The Target Type.",
    )


@func.set_output
class Outputs(CoreModel):
    output_video: Video = Field(..., description="Converted Video.")
