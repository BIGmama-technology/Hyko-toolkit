from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="reverse",
    task="text_utils",
    description="Reverse a given string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    reversed: str = Field(..., description="Reversed input string")


@func.on_call
async def call(inputs: Inputs, params: CoreModel) -> Outputs:
    return Outputs(reversed=inputs.text[::-1])
