from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="max_list",
    task="list_utils",
    cost=0,
    description="Gets the maximum value of a list of numbers.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[float] = field(description="The original list.")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: float = field(
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=max(lst))
