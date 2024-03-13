from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="round",
    task="math_utils",
    description="Round an input number",
)


class RoundOperation(str, Enum):
    FLOOR = "Round down"
    CEILING = "Round up"
    ROUND = "Round"


@func.set_input
class Inputs(CoreModel):
    a: float = Field(..., description="Input number")


@func.set_param
class Params(CoreModel):
    operation: RoundOperation = Field(..., description="Rounding operation")


@func.set_output
class Outputs(CoreModel):
    result: float = Field(..., description="Rounded number result")
