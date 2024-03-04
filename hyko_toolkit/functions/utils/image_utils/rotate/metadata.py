from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Rotate an image by a given angle",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be rotated")


@func.set_param
class Params(CoreModel):
    rotation_angle: int = Field(..., description="Rotation angle in degrees")


@func.set_output
class Outputs(CoreModel):
    rotated_image: Image = Field(..., description="Rotated image")
