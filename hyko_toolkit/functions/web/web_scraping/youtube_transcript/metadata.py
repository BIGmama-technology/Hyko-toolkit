from enum import Enum

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


func = ToolkitFunction(
    name="youtube_transcript",
    task="web_scraping",
    description="Transcript extraction from youtube video.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/web/web_scraping/youtube_transcript/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/web/web_scraping/youtube_transcript",
)


@func.set_input
class Inputs(CoreModel):
    video_url: str = Field(..., description="Youtube Video Id.")


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = Field(..., description="Language Id.")


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="Result")
