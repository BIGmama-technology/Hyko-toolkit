from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

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
    operation: RoundOperation = Field(
        default=RoundOperation.ROUND, description="Rounding operation"
    )


@func.set_output
class Outputs(CoreModel):
    result: float = Field(..., description="Rounded number result")
