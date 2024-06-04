from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Concat",
    task="Text utils",
    category=Category.UTILS,
    cost=0,
    description="Concatenate two strings together",
)


@func.set_input
class Inputs(CoreModel):
    first: str = field(
        description="First string",
        component=TextField(placeholder="Enter your first string here"),
    )
    second: str = field(
        description="Second string",
        component=TextField(placeholder="Enter your second string here"),
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: str = field(description="Concatenated result")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(output=inputs.first + inputs.second)
