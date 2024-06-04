from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Pop element",
    task="List utils",
    category=Category.UTILS,
    cost=0,
    description="Removes an element from a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )


@func.set_param
class Params(CoreModel):
    index: int = field(
        default=-1,
        description="The index of the element to be removed.",
    )


@func.set_output
class Outputs(CoreModel):
    output: list[Any] = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.pop(params.index)
    return Outputs(output=lst)
