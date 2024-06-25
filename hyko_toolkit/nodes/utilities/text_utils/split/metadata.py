from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Split",
    cost=0,
    description="Split a string to a list of strings based on delimiter",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here"),
    )


@node.set_param
class Params(CoreModel):
    delimiter: str = field(
        default=",", description="the string used to split the text by"
    )


@node.set_output
class Outputs(CoreModel):
    splitted: list[str] = field(
        description="List of strings that resulted from splitting by the delimeter"
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(splitted=inputs.text.split(params.delimiter))
