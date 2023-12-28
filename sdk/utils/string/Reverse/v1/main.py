from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Reverse a given string",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    reversed: str = Field(..., description="Reversed input string")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(reversed=inputs.text[::-1])
