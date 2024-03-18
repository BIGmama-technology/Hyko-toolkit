import math
from typing import Callable

from fastapi import HTTPException
from metadata import Inputs, MathOperation, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
