from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate a range of integers",
    requires_gpu=False,
)


class Inputs(CoreModel):
    pass


class Params(CoreModel):
    start: int = Field(..., description="Start integer in the range")
    end: int = Field(..., description="End integer (not included in the range)")


class Outputs(CoreModel):
    result: list[int] = Field(..., description="Output range")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    min_val = params.start
    max_val = params.end
    if min_val > max_val:
        raise HTTPException(status_code=500, detail="start can not be greater than end")
    result = list(range(min_val, max_val))

    return Outputs(result=result)
