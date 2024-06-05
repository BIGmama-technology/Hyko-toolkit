from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Append element",
    cost=0,
    description="Appends an element to a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The list to be appended to.",
    )
    element: Any = field(
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


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.append(inputs.element)
    return Outputs(output=lst)
