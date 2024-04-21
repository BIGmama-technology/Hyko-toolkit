from fastapi.exceptions import HTTPException
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="slice",
    task="text_utils",
    description="Create a slice of a given string of text",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to be sliced")


@func.set_param
class Params(CoreModel):
    start: int = Field(default=None, description="Starting position for slicing")
    length: int = Field(default=None, description="Length of the slice")


@func.set_output
class Outputs(CoreModel):
    output_text: str = Field(..., description="Text slice result")


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
