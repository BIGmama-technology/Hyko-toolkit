from typing import Any

from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="slice_list",
    task="list_utils",
    cost=0,
    description="Slices a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(description="The original list.")


@func.set_param
class Params(CoreModel):
    start: int = field(
        default=0,
        description="The start index of the slice.",
    )
    stop: int = field(
        default=None,
        description="The stop index of the slice.",
    )
    step: int = field(
        default=1,
        description="The step of the slice.",
    )


@func.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=lst[params.start : params.stop : params.step])
