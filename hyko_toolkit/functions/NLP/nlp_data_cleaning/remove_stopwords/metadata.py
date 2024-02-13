from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(description="A function to remove stopwords from text.")


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="The input text from which stopwords are to be removed.",
    )


@func.set_param
class Params(CoreModel):
    language: str = Field(
        ...,
        description="The language of the stopwords. EXAMPLE: Arabic.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The text with stopwords removed.")
