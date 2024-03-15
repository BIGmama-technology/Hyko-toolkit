from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveInt

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
    caption: str = Field(..., description="Caption text to be added")


@func.set_param
class Params(CoreModel):
    caption_size: PositiveInt = Field(default=100, description="Caption size in pixels")
    position: CaptionPosition = Field(
        CaptionPosition.BOTTOM, description="Position to add the caption"
    )
    caption_color: CaptionColor = Field(
        default=CaptionColor.WHITE, description="Caption color: white or black"
    )


@func.set_output
class Outputs(CoreModel):
    captioned_image: Image = Field(..., description="Image with added caption")
