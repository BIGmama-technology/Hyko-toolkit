from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Concat",
    cost=0,
    description="Concatenate two strings together",
)


@node.set_input
class Inputs(CoreModel):
    first: str = field(
        description="First string",
        component=TextField(placeholder="Enter your first string here"),
    )
    second: str = field(
        description="Second string",
        component=TextField(placeholder="Enter your second string here"),
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output: str = field(description="Concatenated result")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(output=inputs.first + inputs.second)
