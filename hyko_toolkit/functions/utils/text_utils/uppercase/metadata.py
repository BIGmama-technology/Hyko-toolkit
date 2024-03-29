from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="uppercase",
    task="text_utils",
    description="Convert a given string to uppercase",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_output
class Outputs(CoreModel):
    uppercase_string: str = Field(
        ..., description="Uppercase version of the input string"
    )
