from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="slice",
    task="text_utils",
    description="Create a slice of a given string of text",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to be sliced")


@func.set_param
class Params(CoreModel):
    start: int = Field(default=None, description="Starting position for slicing")
    length: int = Field(default=None, description="Length of the slice")


@func.set_output
class Outputs(CoreModel):
    output_text: str = Field(..., description="Text slice result")
