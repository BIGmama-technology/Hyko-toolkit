from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Concatenate two strings together",
    requires_gpu=False,
)


class Inputs(CoreModel):
    pass


class Params(CoreModel):
    first: str = Field(..., description="First string")
    second: str = Field(..., description="Second string")


class Outputs(CoreModel):
    output: str = Field(..., description="Concatenated result")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(output=params.first + params.second)
