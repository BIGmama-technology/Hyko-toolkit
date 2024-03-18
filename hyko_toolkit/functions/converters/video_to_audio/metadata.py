from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Audio, Video
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="video_to_audio",
    task="converters",
    description="Convert a video type to audio type (takes only the audio data)",
)


@func.set_input
class Inputs(CoreModel):
    video: Video = Field(..., description="User input video to be converted to audio")


@func.set_output
class Outputs(CoreModel):
    audio: Audio = Field(..., description="converted audio")
