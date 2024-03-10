from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="caption",
    task="image_utils",
    description="Add caption to an image",
)


class CaptionColor(str, Enum):
    WHITE = "white"
    BLACK = "black"


class CaptionPosition(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image to add a caption to")


@func.set_param
class Params(CoreModel):
    caption: str = Field(..., description="Caption text to be added")
    caption_size: int = Field(..., description="Caption size in pixels")
    caption_color: CaptionColor = Field(
        ..., description="Caption color: white or black"
    )
    position: CaptionPosition = Field(..., description="Position to add the caption")


@func.set_output
class Outputs(CoreModel):
    captioned_image: Image = Field(..., description="Image with added caption")
