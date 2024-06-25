from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Remove Stopwords",
    cost=3,
    description="A function to remove stopwords from text.",
    require_worker=True,
)


class SupportedLanguages(str, Enum):
    english = "english"
    arabic = "arabic"
    french = "french"


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="The input text from which stopwords are to be removed.",
        component=TextField(placeholder="Entre your text here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(description="The language of the stopwords.")


@node.set_output
class Outputs(CoreModel):
    result: str = field(description="The text with stopwords removed.")
