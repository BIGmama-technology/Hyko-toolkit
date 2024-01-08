from typing import List

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Join a list of strings with a specified delimiter",
    requires_gpu=False,
)


class Inputs(CoreModel):
    strings: List[str] = Field(..., description="List of strings to join")


class Params(CoreModel):
    delimiter: str = Field(
        default=" ", description="Delimiter used to join the strings"
    )


class Outputs(CoreModel):
    joined_string: str = Field(
        ..., description="String joined with the specified delimiter"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(joined_string=params.delimiter.join(inputs.strings))
