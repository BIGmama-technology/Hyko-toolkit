from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    min_val = params.start
    max_val = params.end
    if min_val > max_val:
        raise HTTPException(status_code=500, detail="start can not be greater than end")
    result = list(range(min_val, max_val))

    return Outputs(result=result)
