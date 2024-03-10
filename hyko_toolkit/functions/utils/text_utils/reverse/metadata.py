from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
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
