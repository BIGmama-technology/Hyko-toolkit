from typing import Any

from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="sort_list",
    task="list_utils",
    cost=0,
    description="Sorts a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list.copy()
    lst.sort(key=None, reverse=False)
    return Outputs(output=lst)
