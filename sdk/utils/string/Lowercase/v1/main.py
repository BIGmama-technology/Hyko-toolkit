from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Convert a given string to lowercase",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    lowercase_string: str = Field(
        ..., description="Lowercase version of the input string"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    lowercase_string = inputs.text.lower()
    return Outputs(lowercase_string=lowercase_string)
