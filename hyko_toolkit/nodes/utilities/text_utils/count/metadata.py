from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Count",
    cost=0,
    description="Count the number of occurrences of a substring in a string",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Your text to count",
        component=TextField(placeholder="Enter your text here"),
    )


@node.set_param
class Params(CoreModel):
    substring: str = field(description="The substring to count")


@node.set_output
class Outputs(CoreModel):
    count: int = field(description="Number of occurrences of the substring")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(count=inputs.text.count(params.substring))
