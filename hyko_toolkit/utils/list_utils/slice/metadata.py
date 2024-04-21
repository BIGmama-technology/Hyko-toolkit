from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="slice_list",
    task="list_utils",
    description="Slices a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(..., description="The original list.")


@func.set_param
class Params(CoreModel):
    start: int = Field(
        default=0,
        description="The start index of the slice.",
    )
    stop: int = Field(
        default=None,
        description="The stop index of the slice.",
    )
    step: int = Field(
        default=1,
        description="The step of the slice.",
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
    return Outputs(output=lst[params.start : params.stop : params.step])
