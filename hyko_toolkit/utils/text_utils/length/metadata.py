from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="length",
    task="text_utils",
    description="Calculate the length of a string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    length: int = Field(..., description="Length of the input string")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(length=len(inputs.text))
