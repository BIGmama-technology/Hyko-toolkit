from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="pop_element",
    task="list_utils",
    description="Removes an element from a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(
        ...,
        description="The original list.",
    )


@func.set_param
class Params(CoreModel):
    index: int = Field(
        default=-1,
        description="The index of the element to be removed.",
    )


@func.set_output
class Outputs(CoreModel):
    output: Any = Field(
        ...,
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.pop(params.index)
    return Outputs(output=lst)
