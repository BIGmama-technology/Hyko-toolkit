from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.models import CoreModel


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


func = SDKFunction(description="Transcript extraction from youtube video.")


@func.set_input
class Inputs(CoreModel):
    video_url: str = Field(
        ...,
        description="Youtube Video Id.",
    )


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = Field(
        ...,
        description="Language Id.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="Result")
