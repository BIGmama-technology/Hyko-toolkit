from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Count",
    cost=0,
    description="Count the number of occurrences of a substring in a string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Your text to count",
        component=TextField(placeholder="Enter your text here"),
    )


@func.set_param
class Params(CoreModel):
    substring: str = field(description="The substring to count")


@func.set_output
class Outputs(CoreModel):
    count: int = field(description="Number of occurrences of the substring")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(count=inputs.text.count(params.substring))