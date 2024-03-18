from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveInt

func = ToolkitFunction(
    name="corp_border",
    task="image_utils",
    description="Remove a specified amount of pixels from all four borders of an image",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    cropped_width: PositiveInt = Field(
        default=0, description="Number of pixels to drop from all four borders"
    )
    cropped_hight: PositiveInt = Field(
        default=0, description="Number of pixels to drop from all four borders"
    )


@func.set_output
class Outputs(CoreModel):
    cropped_image: Image = Field(..., description="Output image")
