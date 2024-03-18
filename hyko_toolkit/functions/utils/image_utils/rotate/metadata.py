from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="rotate",
    task="image_utils",
    description="Rotate an image by a given angle",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be rotated")


@func.set_param
class Params(CoreModel):
    rotation_angle: int = Field(default=30, description="Rotation angle in degrees")


@func.set_output
class Outputs(CoreModel):
    rotated_image: Image = Field(..., description="Rotated image")
