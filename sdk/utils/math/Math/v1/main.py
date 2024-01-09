import math

from fastapi import HTTPException
from metadata import Inputs, MathOperation, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:  # noqa: C901
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
