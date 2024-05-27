from typing import Any

from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="pop_element",
    task="list_utils",
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
    output: Any = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.pop(params.index)
    return Outputs(output=lst)
