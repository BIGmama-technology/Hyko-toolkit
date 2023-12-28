import math
from enum import Enum

from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Perform mathematical operations on numbers",
    requires_gpu=False,
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


class Inputs(CoreModel):
    a: int = Field(..., description="Operand a")
    b: int = Field(..., description="Operand b")


class Params(CoreModel):
    operation: MathOperation = Field(..., description="Mathematical operation")


class Outputs(CoreModel):
    result: int = Field(..., description="Mathematical operation result")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    a = inputs.a
    op = params.operation
    b = inputs.b

    if op == MathOperation.ADD:
        result = a + b
    elif op == MathOperation.SUBTRACT:
        result = a - b
    elif op == MathOperation.MULTIPLY:
        result = a * b
    elif op == MathOperation.DIVIDE:
        if b == 0:
            raise HTTPException(
                status_code=500, detail="Division by zero is not allowed"
            )
        result = a / b
    elif op == MathOperation.POWER:
        result = a**b
    elif op == MathOperation.LOG:
        if a <= 0 or b <= 0:
            raise HTTPException(
                status_code=500,
                detail="Both base and value must be positive for logarithm",
            )

        result = math.log(b, a)
    elif op == MathOperation.MAXIMUM:
        result = max(a, b)
    elif op == MathOperation.MINIMUM:
        result = min(a, b)
    elif op == MathOperation.MODULO:
        result = a % b
    elif op == MathOperation.PERCENT:
        result = a * b / 100
    else:
        raise HTTPException(status_code=500, detail=f"Unknown operator {op}")

    return Outputs(result=result)
