from typing import Any

from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="any_value",
    task="list_utils",
    cost=0,
    description="Returns True if any element of the list is equal a certain value.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )
    value: Any = field(
        description="The value to be checked.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: bool = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=any(element == inputs.value for element in lst))
