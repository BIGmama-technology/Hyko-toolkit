from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Sort list",
    cost=0,
    description="Sorts a list.",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list.copy()
    lst.sort(key=None, reverse=False)
    return Outputs(output=lst)
