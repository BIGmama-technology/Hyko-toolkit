from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="resize_factor",
    task="image_utils",
    description="Resize an image by a factor",
)


class InterpolationMethod(str, Enum):
    Area = "area"
    Linear = "linear"
    Lanczos = "lanczos"
    NearestNeighbor = "nearest-neighbor"
    Cubic = "cubic"


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to resize")


@func.set_param
class Params(CoreModel):
    scale_factor: float = Field(..., description="Scaling factor for resizing")
    interpolation: InterpolationMethod = Field(
        ..., description="Interpolation method for resizing"
    )


@func.set_output
class Outputs(CoreModel):
    resized_image: Image = Field(..., description="Resized image")
