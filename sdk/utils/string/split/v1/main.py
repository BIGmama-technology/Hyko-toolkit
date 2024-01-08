from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Split a string to a list of strings based on delimiter",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    delimeter: str = Field(
        default=",", description="the string used to split the text by"
    )


class Outputs(CoreModel):
    splitted: list[str] = Field(
        ..., description="List of strings that resulted from splitting by the delimeter"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(splitted=inputs.text.split(params.delimeter))
