from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Insert element",
    task="List utils",
    category=Category.UTILS,
    cost=0,
    description="Inserts an element to a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The list to be extended.",
    )
    element: Any = field(
        description="The element to be inserted into the list.",
    )


@func.set_param
class Params(CoreModel):
    index: int = field(
        description="The index of the element to be inserted.",
    )


@func.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.insert(params.index, inputs.element)
    return Outputs(output=lst)
