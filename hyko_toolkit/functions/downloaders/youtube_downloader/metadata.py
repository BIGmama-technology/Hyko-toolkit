from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction


class Resolution(str, Enum):
    p720 = "720p"
    p360 = "360p"
    p144 = "144p"
    highest = "highest"
    lowest = "lowest"


func = ToolkitFunction(
    name="youtube_downloader",
    task="downloaders",
    description="Download a video from YouTube.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/downloaders/youtube_downloader/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/downloaders/youtube_downloader",
)


@func.set_input
class Inputs(CoreModel):
    video_url: str = field(
        description="The URL of the YouTube video to download.",
        component=TextField(placeholder="Entre your URL here"),
    )


@func.set_param
class Params(CoreModel):
    resolution: Resolution = field(description="The desired resolution of the video.")


@func.set_output
class Outputs(CoreModel):
    output_video: Video = field(description="Output Video.")
