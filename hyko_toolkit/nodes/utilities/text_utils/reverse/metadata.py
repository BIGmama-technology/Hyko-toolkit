from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Reverse",
    cost=0,
    description="Reverse a given string",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here"),
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    reversed: str = field(description="Reversed input string")


@node.on_call
async def call(inputs: Inputs, params: CoreModel) -> Outputs:
    return Outputs(reversed=inputs.text[::-1])
