from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Convert a given string to uppercase",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    uppercase_string: str = Field(
        ..., description="Uppercase version of the input string"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(uppercase_string=inputs.text.upper())
