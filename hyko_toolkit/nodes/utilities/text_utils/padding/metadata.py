from enum import Enum

from fastapi import HTTPException
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Padding",
    cost=0,
    description="Pads text until it has a certain length",
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text to be padded",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


class PaddingAlignment(str, Enum):
    START = "start"
    END = "end"
    CENTER = "center"


@node.set_param
class Params(CoreModel):
    width: int = field(description="Width of the padded text")
    padding: str = field(description="Padding character")
    alignment: PaddingAlignment = field(
        default=PaddingAlignment.START, description="Padding alignment"
    )


@node.set_output
class Outputs(CoreModel):
    output_text: str = field(description="Padded text result")


@node.on_call
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
