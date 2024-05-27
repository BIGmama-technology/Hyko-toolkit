from hyko_sdk.io import Audio, Video
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Video to audio",
    task="Converters",
    category=Category.FUNCTION,
    cost=3,
    description="Convert a video type to audio type (takes only the audio data)",
    icon="video",
)


@func.set_input
class Inputs(CoreModel):
    video: Video = field(description="User input video to be converted to audio")


@func.set_output
class Outputs(CoreModel):
    audio: Audio = field(description="converted audio")
