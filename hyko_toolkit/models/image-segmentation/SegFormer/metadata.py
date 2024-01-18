from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Image Segmentation Model, this models takes an image and partition it to locate objects and their contours in the image",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="User inputted image to be segmented")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    segmented_image: Image = Field(..., description="Segmented image")
