from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Max list",
    cost=0,
    description="Gets the maximum value of a list of numbers.",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[float] = field(description="The original list.")


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output: float = field(
        description="Final list.",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=max(lst))
