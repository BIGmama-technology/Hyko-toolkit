from fastapi import HTTPException
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Range",
    cost=0,
    description="Generate a range of integers",
)


@node.set_input
class Inputs(CoreModel):
    pass


@node.set_param
class Params(CoreModel):
    start: int = field(description="Start integer in the range")
    end: int = field(description="End integer (not included in the range)")


@node.set_output
class Outputs(CoreModel):
    result: list[int] = field(description="Output range")


@node.on_call
async def call(inputs: CoreModel, params: Params) -> Outputs:
    min_val = params.start
    max_val = params.end
    if min_val > max_val:
        raise HTTPException(status_code=500, detail="start can not be greater than end")
    result = list(range(min_val, max_val))

    return Outputs(result=result)
