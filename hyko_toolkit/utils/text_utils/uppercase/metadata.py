from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="uppercase",
    task="text_utils",
    description="Convert a given string to uppercase",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    uppercase_string: str = Field(
        ..., description="Uppercase version of the input string"
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(uppercase_string=inputs.text.upper())
