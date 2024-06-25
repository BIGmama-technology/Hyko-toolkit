from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Uppercase",
    cost=0,
    description="Convert a given string to uppercase",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    uppercase_string: str = field(description="Uppercase version of the input string")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(uppercase_string=inputs.text.upper())
