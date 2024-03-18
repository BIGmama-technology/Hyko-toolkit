from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="remove_stopwords",
    task="nlp_utils",
    description="A function to remove stopwords from text.",
)


class SupportedLanguages(str, Enum):
    english = "english"
    arabic = "arabic"
    french = "french"


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="The input text from which stopwords are to be removed.",
    )


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = Field(
        ...,
        description="The language of the stopwords.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The text with stopwords removed.")
