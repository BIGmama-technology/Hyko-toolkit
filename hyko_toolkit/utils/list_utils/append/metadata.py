from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="append_element",
    task="list_utils",
    description="Appends an element to a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(
        ...,
        description="The list to be appended to.",
    )
    element: Any = Field(
        ...,
        description="List of elements to be appended to the original list.",
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
    lst.append(inputs.element)
    return Outputs(output=lst)
