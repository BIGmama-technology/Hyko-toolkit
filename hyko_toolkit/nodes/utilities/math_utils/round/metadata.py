import math
from enum import Enum

from fastapi import HTTPException
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Round",
    cost=0,
    description="Round an input number",
)


class RoundOperation(str, Enum):
    FLOOR = "Round down"
    CEILING = "Round up"
    ROUND = "Round"


@node.set_input
class Inputs(CoreModel):
    a: float = field(description="Input number")


@node.set_param
class Params(CoreModel):
    operation: RoundOperation = field(
        default=RoundOperation.ROUND, description="Rounding operation"
    )


@node.set_output
class Outputs(CoreModel):
    result: float = field(description="Rounded number result")


def round_half_up(x: float) -> float:
    return math.floor(x + 0.5)


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
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
