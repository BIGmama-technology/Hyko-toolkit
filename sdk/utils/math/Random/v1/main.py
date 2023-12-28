from random import randint

from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate a random integer",
    requires_gpu=False,
)


class Inputs(CoreModel):
    pass


class Params(CoreModel):
    min_val: int = Field(..., description="Minimum value for random number generation")
    max_val: int = Field(..., description="Maximum value for random number generation")


class Outputs(CoreModel):
    result: int = Field(..., description="Generated random number")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    min_val = params.min_val
    max_val = params.max_val
    if min_val > max_val:
        raise HTTPException(
            status_code=500, detail="min_val can not be greater than max_val"
        )
    result = randint(min_val, max_val)

    return Outputs(result=result)
