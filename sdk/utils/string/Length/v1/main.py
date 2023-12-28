from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Calculate the length of a string",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    length: int = Field(..., description="Length of the input string")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(length=len(inputs.text))
