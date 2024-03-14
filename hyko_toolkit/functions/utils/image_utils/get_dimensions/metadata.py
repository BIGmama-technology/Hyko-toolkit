from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="get_dimensions",
    task="image_utils",
    description="Get the Height, Width, and number of Channels from an image",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to get dimensions from")


@func.set_output
class Outputs(CoreModel):
    width: int = Field(..., description="Width of the image")
    height: int = Field(..., description="Height of the image")
    channels: int = Field(..., description="Number of channels in the image")
