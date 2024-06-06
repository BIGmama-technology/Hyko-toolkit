from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Audio, Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Video to audio",
    cost=3,
    description="Convert a video type to audio type (takes only the audio data)",
    icon="video",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    video: Video = field(description="User input video to be converted to audio")


@node.set_output
class Outputs(CoreModel):
    audio: Audio = field(description="converted audio")
