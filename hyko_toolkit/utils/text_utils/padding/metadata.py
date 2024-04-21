from enum import Enum

from fastapi import HTTPException
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="padding",
    task="text_utils",
    description="Pads text until it has a certain length",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to be padded")


class PaddingAlignment(str, Enum):
    START = "start"
    END = "end"
    CENTER = "center"


@func.set_param
class Params(CoreModel):
    width: int = Field(..., description="Width of the padded text")
    padding: str = Field(..., description="Padding character")
    alignment: PaddingAlignment = Field(
        default=PaddingAlignment.START, description="Padding alignment"
    )


@func.set_output
class Outputs(CoreModel):
    output_text: str = Field(..., description="Padded text result")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    text = inputs.text
    width = params.width
    padding = params.padding
    alignment = params.alignment

    if alignment == PaddingAlignment.START:
        result = text.rjust(width, padding)
    elif alignment == PaddingAlignment.END:
        result = text.ljust(width, padding)
    elif alignment == PaddingAlignment.CENTER:
        result = text.center(width, padding)
    else:
        raise HTTPException(status_code=500, detail=f"Invalid alignment '{alignment}'.")

    return Outputs(output_text=result)
