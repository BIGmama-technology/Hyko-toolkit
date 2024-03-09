from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.models import CoreModel

func = SDKFunction(description="A function to remove stopwords from text.")


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


@func.set_startup_params
class StartupParams(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = Field(
        ...,
        description="The language of the stopwords.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The text with stopwords removed.")
