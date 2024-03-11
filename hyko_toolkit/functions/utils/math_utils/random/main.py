from random import randint

from fastapi import HTTPException
from metadata import Outputs, Params, func

from hyko_sdk.models import CoreModel


@func.on_execute
async def main(inputs: CoreModel, params: Params) -> Outputs:
    min_val = params.min_val
    max_val = params.max_val
    if min_val > max_val:
        raise HTTPException(
            status_code=500, detail="min_val can not be greater than max_val"
        )
    result = randint(min_val, max_val)

    return Outputs(result=result)
