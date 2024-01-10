from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Remove a specified amount of pixels from all four borders of an image",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    amount: int = Field(
        ..., description="Number of pixels to drop from all four borders"
    )


@func.set_output
class Outputs(CoreModel):
    cropped_image: Image = Field(..., description="Output image")
