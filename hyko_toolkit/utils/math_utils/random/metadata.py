from random import randint

from fastapi import HTTPException
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="random",
    task="math_utils",
    description="Generate a random integer",
)


@func.set_input
class Inputs(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    min_val: int = field(description="Minimum value for random number generation")
    max_val: int = field(description="Maximum value for random number generation")


@func.set_output
class Outputs(CoreModel):
    result: int = field(description="Generated random number")


@func.on_call
async def call(inputs: CoreModel, params: Params) -> Outputs:
    min_val = params.min_val
    max_val = params.max_val
    if min_val > max_val:
        raise HTTPException(
            status_code=500, detail="min_val can not be greater than max_val"
        )
    result = randint(min_val, max_val)

    return Outputs(result=result)
