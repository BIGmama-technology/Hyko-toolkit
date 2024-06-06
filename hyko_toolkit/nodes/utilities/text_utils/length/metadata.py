from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Length",
    cost=0,
    description="Calculate the length of a string",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text to calculate the length of",
        component=TextField(placeholder="Enter your text here"),
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    length: int = field(description="Length of the input string")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(length=len(inputs.text))
