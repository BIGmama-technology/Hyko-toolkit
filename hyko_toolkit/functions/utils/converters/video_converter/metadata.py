from enum import Enum

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Video
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Convert a video from one format to another.",
)


class SupportedTypes(str, Enum):
    # mkv = "mkv"
    # mov = "mov"
    # avi = "avi"
    mp4 = "mp4"
    # wmv = "wmv"
    webm = "webm"


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
