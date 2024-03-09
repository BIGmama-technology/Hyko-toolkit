from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel

func = SDKFunction(
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
        ..., description="Flip axis: horizontal, vertical, both, or none"
    )


@func.set_output
class Outputs(CoreModel):
    flipped_image: Image = Field(..., description="Output image")
