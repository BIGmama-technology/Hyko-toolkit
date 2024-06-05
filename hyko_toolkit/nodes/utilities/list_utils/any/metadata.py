from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Any value",
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
