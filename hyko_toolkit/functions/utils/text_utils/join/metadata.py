from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="join",
    task="text_utils",
    description="Join a list of strings with a specified delimiter",
)


@func.set_input
class Inputs(CoreModel):
    strings: list[str] = Field(..., description="List of strings to join")


@func.set_param
class Params(CoreModel):
    delimiter: str = Field(
        default=" ", description="Delimiter used to join the strings"
    )


@func.set_output
class Outputs(CoreModel):
    joined_string: str = Field(
        ..., description="String joined with the specified delimiter"
    )
