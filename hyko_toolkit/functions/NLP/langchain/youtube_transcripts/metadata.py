from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(description="Transcript extraction from youtube video.")


@func.set_input
class Inputs(CoreModel):
    url: str = Field(
        ...,
        description="Youtube URL. ",
    )


@func.set_param
class Params(CoreModel):
    language: str = Field(
        ...,
        description="Originale Language Id .example : en , ar.",
    )
    translation: str = Field(
        ...,
        description="Translation Language Id .example : en , ar",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="Result")
