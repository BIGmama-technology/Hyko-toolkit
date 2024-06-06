import re

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Remove special characters",
    cost=0,
    description="A function to remove special characters and punctuation from text.",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="The input text from which special characters and punctuation will be removed.",
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    result: str = field(
        description="The text with special characters and punctuation removed."
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    # Define the regular expression pattern to match non-alphanumeric characters (excluding spaces)
    pattern = r"[^a-zA-Z0-9\s]"

    # Replace non-alphanumeric characters with an empty string
    cleaned_text = re.sub(pattern, "", inputs.text)

    return Outputs(result=" ".join(cleaned_text.strip().split()))
