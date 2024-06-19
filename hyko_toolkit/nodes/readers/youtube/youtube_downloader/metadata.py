from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field


class Resolution(str, Enum):
    p720 = "720p"
    p360 = "360p"
    p144 = "144p"
    highest = "highest"
    lowest = "lowest"


node = ToolkitNode(
    name="Youtube downloader",
    cost=2,
    description="Download a video from YouTube.",
    icon="youtube",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    video_url: str = field(
        description="The URL of the YouTube video to download.",
        component=TextField(placeholder="Entre your URL here"),
    )


@node.set_param
class Params(CoreModel):
    resolution: Resolution = field(description="The desired resolution of the video.")


@node.set_output
class Outputs(CoreModel):
    output_video: Video = field(description="Output Video.")
