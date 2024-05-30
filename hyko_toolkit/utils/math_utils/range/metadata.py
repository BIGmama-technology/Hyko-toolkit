from fastapi import HTTPException
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Range",
    task="Math utils",
    category=Category.UTILS,
    cost=0,
    description="Generate a range of integers",
)


@func.set_input
class Inputs(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    start: int = field(description="Start integer in the range")
    end: int = field(description="End integer (not included in the range)")


@func.set_output
class Outputs(CoreModel):
    result: list[int] = field(description="Output range")


@func.on_call
async def call(inputs: CoreModel, params: Params) -> Outputs:
    min_val = params.start
    max_val = params.end
    if min_val > max_val:
        raise HTTPException(status_code=500, detail="start can not be greater than end")
    result = list(range(min_val, max_val))

    return Outputs(result=result)
