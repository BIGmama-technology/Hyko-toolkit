from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Count the number of occurrences of a substring in a string",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    substring: str = Field(..., description="The substring to count")


class Outputs(CoreModel):
    count: int = Field(..., description="Number of occurrences of the substring")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(count=inputs.text.count(params.substring))
