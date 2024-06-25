from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Count element",
    cost=0,
    description="Counts the number of occurrences of an element in a list.",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )
    element: Any = field(
        description="The element to be counted in the list.",
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output: int = field(
        description="Final list.",
    )


def count_element(lst: list[Any], element: Any) -> int:
    return lst.count(element)


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=lst.count(inputs.element))
