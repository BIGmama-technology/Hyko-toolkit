from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Index element",
    cost=0,
    description="Returns the index of an element in a list.",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )
    element: Any = field(
        description="The element to be found in the list.",
    )


@node.set_param
class Params(CoreModel):
    start: int = field(
        default=0,
        description="The start index of the slice.",
    )
    end: int = field(
        default=0,
        description="The stop index of the slice.",
    )


@node.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=lst.index(inputs.element, params.start, params.end))
