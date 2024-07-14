import re

from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Regex",
    cost=0,
    description="Node to perform regex matching on input text and extract matching patterns.",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text input for regex matching",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    regex: str = field(
        description="Regular expression pattern to extract from the text."
    )


@node.set_output
class Outputs(CoreModel):
    output_text: list[str] = field(
        description="List of strings matching the regex pattern in the input text.",
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    text = inputs.text
    regex = params.regex
    result = re.findall(regex, text)
    return Outputs(output_text=result)
