from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="remove_stopwords",
    task="nlp_utils",
    cost=3,
    description="A function to remove stopwords from text.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/nlp_utils/remove_stopwords/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/nlp_utils/remove_stopwords",
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
