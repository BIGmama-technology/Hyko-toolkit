from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Lowercase",
    cost=0,
    description="Convert a given string to lowercase",
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
    lowercase_string: str = field(description="Lowercase version of the input string")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lowercase_string = inputs.text.lower()
    return Outputs(lowercase_string=lowercase_string)
