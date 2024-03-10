from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="shift",
    task="image_utils",
    description="Shift an image by a given amount in X and Y directions",
)


class FillColor(str, Enum):
    AUTO = "auto"
    BLACK = "black"
    TRANSPARENT = "transparent"

    def get_color(self, channels: int):
        """Select how to fill negative space that results from shifting"""

        if self == FillColor.AUTO:
            fill_color = (0,) * channels
        elif self == FillColor.BLACK:
            fill_color = (0,) * channels if channels < 4 else (0, 0, 0, 1)
        else:
            fill_color = (0, 0, 0, 0)

        return fill_color


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be shifted")


@func.set_param
class Params(CoreModel):
    amount_x: int = Field(..., description="Shift amount in the X direction")
    amount_y: int = Field(..., description="Shift amount in the Y direction")
    negative_space_fill: FillColor = Field(
        ..., description="Fill color for shifted area"
    )


@func.set_output
class Outputs(CoreModel):
    shifted_image: Image = Field(..., description="Shifted image")
