from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


node = ToolkitNode(
    name="Youtube transcript",
    cost=5,
    description="Transcript extraction from youtube video.",
    icon="youtube",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    video_url: str = field(
        description="Youtube Video Id.",
        component=TextField(placeholder="Enter your video url here"),
    )


@node.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(description="Language Id.")


@node.set_output
class Outputs(CoreModel):
    result: str = field(description="Result")
