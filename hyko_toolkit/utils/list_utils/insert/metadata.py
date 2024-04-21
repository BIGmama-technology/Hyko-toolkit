from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="insert_element",
    task="list_utils",
    description="Inserts an element to a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(
        ...,
        description="The list to be extended.",
    )
    element: Any = Field(
        ...,
        description="The element to be inserted into the list.",
    )


@func.set_param
class Params(CoreModel):
    index: int = Field(
        ...,
        description="The index of the element to be inserted.",
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
    lst.insert(params.index, inputs.element)
    return Outputs(output=lst)
