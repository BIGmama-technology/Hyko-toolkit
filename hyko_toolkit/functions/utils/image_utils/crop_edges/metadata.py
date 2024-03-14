from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="crop_edges",
    task="image_utils",
    description="Crop an image from the specified edges",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    top: int = Field(..., description="Number of pixels to crop from the top")
    left: int = Field(..., description="Number of pixels to crop from the left")
    right: int = Field(..., description="Number of pixels to crop from the right")
    bottom: int = Field(..., description="Number of pixels to crop from the bottom")


@func.set_output
class Outputs(CoreModel):
    cropped_image: Image = Field(..., description="Output cropped image")
