from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="min_list",
    task="list_utils",
    description="Gets the minimum value of a list of numbers.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[float] = Field(..., description="The original list.")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: float = Field(
        ...,
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=min(lst))
