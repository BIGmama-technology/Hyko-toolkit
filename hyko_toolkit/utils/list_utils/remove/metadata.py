from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="remove_element",
    task="list_utils",
    description="Removes an element from a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(..., description="The original list.")
    element: Any = Field(
        ...,
        description="The element to be removed from the list.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: Any = Field(
        ...,
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.remove(inputs.element)
    return Outputs(output=lst)
