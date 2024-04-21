from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="index_element",
    task="list_utils",
    description="Returns the index of an element in a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(
        ...,
        description="The original list.",
    )
    element: Any = Field(
        ...,
        description="The element to be found in the list.",
    )


@func.set_param
class Params(CoreModel):
    start: int = Field(
        default=0,
        description="The start index of the slice.",
    )
    end: int = Field(
        default=0,
        description="The stop index of the slice.",
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
    return Outputs(output=lst.index(inputs.element, params.start, params.end))
