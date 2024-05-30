from fastapi.exceptions import HTTPException
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Slice",
    task="Text utils",
    category=Category.UTILS,
    cost=0,
    description="Create a slice of a given string of text",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text to be sliced",
        component=TextField(placeholder="Enter your text here"),
    )


@func.set_param
class Params(CoreModel):
    start: int = field(default=None, description="Starting position for slicing")
    length: int = field(default=None, description="Length of the slice")


@func.set_output
class Outputs(CoreModel):
    output_text: str = field(description="Text slice result")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    text = inputs.text
    start = params.start
    length = params.length
    if length < 0:
        raise HTTPException(status_code=500, detail="Length must not be less than 0")
    start = max(-len(text), start)
    result = text[start : start + length]

    return Outputs(output_text=result)
