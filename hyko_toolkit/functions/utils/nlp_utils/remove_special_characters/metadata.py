from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="A function to remove special characters and punctuation from text."
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="The input text from which special characters and punctuation will be removed.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    result: str = Field(
        ..., description="The text with special characters and punctuation removed."
    )
