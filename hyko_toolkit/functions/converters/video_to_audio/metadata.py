from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.io import Audio, Video
from hyko_sdk.models import CoreModel

func = SDKFunction(
    description="Convert a video type to audio type (takes only the audio data)",
)


@func.set_input
class Inputs(CoreModel):
    video: Video = Field(..., description="User input video to be converted to audio")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    audio: Audio = Field(..., description="converted audio")
