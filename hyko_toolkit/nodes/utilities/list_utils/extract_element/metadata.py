from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Extract an element from a list",
    cost=0,
    description="Node to extract a specified element from a list based on the provided index.",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The list from which to extract an element.",
    )


@node.set_param
class Params(CoreModel):
    index: int = field(description="The index of the element to extract from the list.")


@node.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Extracted element from the list based on the provided index.",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    original_list = inputs.original_list
    index = params.index
    return Outputs(output=original_list[index])
