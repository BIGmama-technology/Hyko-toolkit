from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="flip",
    task="image_utils",
    description="Flip an image based on the specified axis",
)


class FlipAxis(str, Enum):
    horizontal = "horizontal"
    vertical = "vertical"
    both = "both"


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    flip_axis: FlipAxis = Field(
        default=FlipAxis.horizontal,
        description="Flip axis: horizontal, vertical, both, or none",
    )


@func.set_output
class Outputs(CoreModel):
    flipped_image: Image = Field(..., description="Output image")
