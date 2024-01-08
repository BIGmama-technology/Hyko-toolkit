from enum import Enum

from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Pads text until it has a certain length",
    requires_gpu=False,
)


class PaddingAlignment(str, Enum):
    START = "start"
    END = "end"
    CENTER = "center"


class Inputs(CoreModel):
    text: str = Field(..., description="Text to be padded")


class Params(CoreModel):
    width: int = Field(..., description="Width of the padded text")
    padding: str = Field(..., description="Padding character")
    alignment: PaddingAlignment = Field(..., description="Padding alignment")


class Outputs(CoreModel):
    output_text: str = Field(..., description="Padded text result")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
