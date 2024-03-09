from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.models import CoreModel

func = SDKFunction(
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
    a: int = Field(..., description="Operand a")
    b: int = Field(..., description="Operand b")


@func.set_param
class Params(CoreModel):
    operation: MathOperation = Field(..., description="Mathematical operation")


@func.set_output
class Outputs(CoreModel):
    result: float = Field(..., description="Mathematical operation result")
