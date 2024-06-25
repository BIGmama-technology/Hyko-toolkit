from typing import Any, Iterable

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Extend list",
    cost=0,
    description="Extends a list with another list.",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The list to be extended.",
    )
    iterable: Any = field(
        description="List of elements to be appended to the original list.",
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


def extend_list(lst: list[Any], iterable: Iterable[Any]) -> list[Any]:
    lst.extend(iterable)
    return lst


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.extend(inputs.iterable)
    return Outputs(output=lst)
