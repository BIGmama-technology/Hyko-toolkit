from enum import Enum
import math
from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction


func = SDKFunction(
    description="Round an input number",
    requires_gpu=False,
)

def round_half_up(x:float)-> float:
    return math.floor(x + 0.5)

class RoundOperation(str,Enum):
    FLOOR = "Round down"
    CEILING = "Round up"
    ROUND = "Round"


class Inputs(CoreModel):
    a: float = Field(..., description="Input number")

class Params(CoreModel): 
    operation: RoundOperation = Field(..., description="Rounding operation")

class Outputs(CoreModel):
    result: float = Field(..., description="Rounded number result")


@func.on_execute
async def main(inputs: Inputs , params: Params)-> Outputs:
    a = inputs.a
    operation = params.operation
   
    if operation == RoundOperation.FLOOR:
        op = math.floor
    elif operation == RoundOperation.CEILING:
        op = math.ceil
    elif operation == RoundOperation.ROUND:
        op = round_half_up
    else:
        
        raise HTTPException(
                    status_code=500,
                    detail=f"Unknown operation {operation}"
                )

    result = op(a)

    return Outputs(result=result)

