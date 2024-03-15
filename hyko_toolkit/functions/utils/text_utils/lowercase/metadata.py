from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="lowercase",
    task="text_utils",
    description="Convert a given string to lowercase",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_output
class Outputs(CoreModel):
    lowercase_string: str = Field(
        ..., description="Lowercase version of the input string"
    )
