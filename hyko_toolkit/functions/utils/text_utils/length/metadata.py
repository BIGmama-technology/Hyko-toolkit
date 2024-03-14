from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="length",
    task="text_utils",
    description="Calculate the length of a string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_output
class Outputs(CoreModel):
    length: int = Field(..., description="Length of the input string")
