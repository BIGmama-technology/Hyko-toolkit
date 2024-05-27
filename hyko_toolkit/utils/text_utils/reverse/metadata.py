from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.UTILS,
    name="reverse",
    task="text_utils",
    cost=0,
    description="Reverse a given string",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here"),
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    reversed: str = field(description="Reversed input string")


@func.on_call
async def call(inputs: Inputs, params: CoreModel) -> Outputs:
    return Outputs(reversed=inputs.text[::-1])
