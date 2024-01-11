import math

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, RoundOperation, func


def round_half_up(x: float) -> float:
    return math.floor(x + 0.5)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    a = inputs.a
    operation = params.operation

    if operation == RoundOperation.FLOOR:
        op = math.floor
    elif operation == RoundOperation.CEILING:
        op = math.ceil
    elif operation == RoundOperation.ROUND:
        op = round_half_up
    else:
        raise HTTPException(status_code=500, detail=f"Unknown operation {operation}")

    result = op(a)

    return Outputs(result=result)
