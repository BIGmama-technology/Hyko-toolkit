from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Length",
    task="Text utils",
    category=Category.UTILS,
    cost=0,
    description="Calculate the length of a string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text to calculate the length of",
        component=TextField(placeholder="Enter your text here"),
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    length: int = field(description="Length of the input string")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(length=len(inputs.text))
