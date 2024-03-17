from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="padding",
    task="image_utils",
    description="Adds padding to an image by a given amount from the left, right, top and bottom",
)


class FillColor(str, Enum):
    BLACK = "black"
    WHITE = "white"
    TRANSPARENT = "transparent"

    def get_color(self):
        """Select how to fill negative space that results from padding"""
        if self == FillColor.WHITE:
            fill_color = (255, 255, 255)
        elif self == FillColor.BLACK:
            fill_color = (0, 0, 0)
        else:
            fill_color = (0, 0, 0, 0)

        return fill_color


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be padded")


@func.set_param
class Params(CoreModel):
    right: int = Field(default=10, description="Padding amount from the right")
    left: int = Field(default=10, description="Padding amount from the left")
    top: int = Field(default=10, description="Padding from the top")
    bottom: int = Field(default=10, description="Padding from the bottom")
    negative_space_fill: FillColor = Field(
        FillColor.WHITE, description="Fill color for padded area"
    )


@func.set_output
class Outputs(CoreModel):
    shifted_image: Image = Field(..., description="Padded image")
