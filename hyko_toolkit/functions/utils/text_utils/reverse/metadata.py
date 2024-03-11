from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="reverse",
    task="text_utils",
    description="Reverse a given string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_output
class Outputs(CoreModel):
    reversed: str = Field(..., description="Reversed input string")
