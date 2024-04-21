from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="concat",
    task="text_utils",
    description="Concatenate two strings together",
)


@func.set_input
class Inputs(CoreModel):
    first: str = Field(..., description="First string")
    second: str = Field(..., description="Second string")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: str = Field(..., description="Concatenated result")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(output=inputs.first + inputs.second)
