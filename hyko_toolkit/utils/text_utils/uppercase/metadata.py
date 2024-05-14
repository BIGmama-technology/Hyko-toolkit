from hyko_sdk.components.components import TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="uppercase",
    task="text_utils",
    cost=0,
    description="Convert a given string to uppercase",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    uppercase_string: str = field(description="Uppercase version of the input string")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(uppercase_string=inputs.text.upper())
