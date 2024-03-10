from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    description="Pads text until it has a certain length",
)


class PaddingAlignment(str, Enum):
    START = "start"
    END = "end"
    CENTER = "center"


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to be padded")


@func.set_param
class Params(CoreModel):
    width: int = Field(..., description="Width of the padded text")
    padding: str = Field(..., description="Padding character")
    alignment: PaddingAlignment = Field(..., description="Padding alignment")


@func.set_output
class Outputs(CoreModel):
    output_text: str = Field(..., description="Padded text result")
