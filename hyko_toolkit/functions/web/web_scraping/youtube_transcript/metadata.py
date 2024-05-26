from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


func = ToolkitFunction(
    name="Youtube transcript",
    task="Web scraping",
    cost=5,
    description="Transcript extraction from youtube video.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/web/web_scraping/youtube_transcript/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/web/web_scraping/youtube_transcript",
    icon="youtube",
)


@func.set_input
class Inputs(CoreModel):
    video_url: str = field(
        description="Youtube Video Id.",
        component=TextField(placeholder="Enter your video url here"),
    )


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(description="Language Id.")


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="Result")
