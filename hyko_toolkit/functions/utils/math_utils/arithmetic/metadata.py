from enum import Enum

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="arithmetic",
    task="math_utils",
    description="Perform mathematical operations on numbers",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/math_utils/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/math_utils/arithmetic",
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
