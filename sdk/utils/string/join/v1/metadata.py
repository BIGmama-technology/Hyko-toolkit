from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
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
