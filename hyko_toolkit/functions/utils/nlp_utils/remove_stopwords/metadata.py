from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Remove Stopwords",
    task="Nlp utils",
    category=Category.FUNCTION,
    cost=3,
    description="A function to remove stopwords from text.",
)


class SupportedLanguages(str, Enum):
    english = "english"
    arabic = "arabic"
    french = "french"


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="The input text from which stopwords are to be removed.",
        component=TextField(placeholder="Entre your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(description="The language of the stopwords.")


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="The text with stopwords removed.")
