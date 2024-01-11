from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Get the Height, Width, and number of Channels from an image",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to get dimensions from")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    width: int = Field(..., description="Width of the image")
    height: int = Field(..., description="Height of the image")
    channels: int = Field(..., description="Number of channels in the image")
