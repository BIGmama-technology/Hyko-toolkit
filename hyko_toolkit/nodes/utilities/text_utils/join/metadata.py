from hyko_sdk.components.components import ListComponent, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Join",
    cost=0,
    description="Join a list of strings with a specified delimiter",
)


@node.set_input
class Inputs(CoreModel):
    strings: list[str] = field(
        description="List of strings to join",
        component=ListComponent(
            item_component=TextField(placeholder="Enter your text here", multiline=True)
        ),
    )


@node.set_param
class Params(CoreModel):
    delimiter: str = field(
        default=" ", description="Delimiter used to join the strings"
    )


@node.set_output
class Outputs(CoreModel):
    joined_string: str = field(description="String joined with the specified delimiter")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(joined_string=params.delimiter.join(inputs.strings))
