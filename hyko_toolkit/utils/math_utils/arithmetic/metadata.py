import math
from enum import Enum
from typing import Callable

from fastapi import HTTPException
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="arithmetic",
    task="math_utils",
    cost=0,
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
    a: float = field(description="Operand a")
    b: float = field(description="Operand b")


@func.set_param
class Params(CoreModel):
    operation: MathOperation = field(
        default=MathOperation.ADD, description="Mathematical operation"
    )


@func.set_output
class Outputs(CoreModel):
    result: float = field(description="Mathematical operation result")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    a = inputs.a
    op = params.operation
    b = inputs.b

    operations: dict[MathOperation, Callable[[float, float], float]] = {
        MathOperation.ADD: lambda a, b: a + b,
        MathOperation.SUBTRACT: lambda a, b: a - b,
        MathOperation.MULTIPLY: lambda a, b: a * b,
        MathOperation.DIVIDE: lambda a, b: a / b,
        MathOperation.POWER: lambda a, b: a**b,
        MathOperation.LOG: lambda a, b: math.log(a, b),
        MathOperation.MAXIMUM: lambda a, b: max(a, b),
        MathOperation.MINIMUM: lambda a, b: min(a, b),
        MathOperation.MODULO: lambda a, b: a % b,
        MathOperation.PERCENT: lambda a, b: a * 100 / b,
    }

    try:
        result = operations[op](a, b)
        return Outputs(result=result)
    except (ValueError, ZeroDivisionError) as exc:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong with the function: {exc}"
        ) from exc
    except KeyError as exc:
        raise HTTPException(status_code=500, detail=f"Unknown operator {op}") from exc
