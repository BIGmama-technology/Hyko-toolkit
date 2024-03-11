from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="concat",
    task="text_utils",
    description="Concatenate two strings together",
)


@func.set_input
class Inputs(CoreModel):
    first: str = Field(..., description="First string")
    second: str = Field(..., description="Second string")


@func.set_output
class Outputs(CoreModel):
    output: str = Field(..., description="Concatenated result")
