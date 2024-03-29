from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="arithmetic",
    task="math_utils",
    description="Perform mathematical operations on numbers",
)


class MathOperation(str, Enum):
    ADD = "add"
    SUBTRACT = "sub"
    MULTIPLY = "mul"
    DIVIDE = "div"
    POWER = "pow"
    LOG = "log"
    MAXIMUM = "max"
    MINIMUM = "min"
    MODULO = "mod"
    PERCENT = "percent"


@func.set_input
class Inputs(CoreModel):
    a: float = Field(..., description="Operand a")
    b: float = Field(..., description="Operand b")


@func.set_param
class Params(CoreModel):
    operation: MathOperation = Field(
        default=MathOperation.ADD, description="Mathematical operation"
    )


@func.set_output
class Outputs(CoreModel):
    result: float = Field(..., description="Mathematical operation result")
