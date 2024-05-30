from typing import Any, Iterable

from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Extend list",
    task="List utils",
    category=Category.UTILS,
    cost=0,
    description="Extends a list with another list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The list to be extended.",
    )
    iterable: Any = field(
        description="List of elements to be appended to the original list.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


def extend_list(lst: list[Any], iterable: Iterable[Any]) -> list[Any]:
    lst.extend(iterable)
    return lst


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.extend(inputs.iterable)
    return Outputs(output=lst)
