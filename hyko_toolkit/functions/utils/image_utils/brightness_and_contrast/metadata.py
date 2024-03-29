from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="brightness_and_contrast",
    task="image_utils",
    description="Adjust brightness and contrast of an image",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(
        ..., description="Input image to adjust brightness and contrast"
    )


@func.set_param
class Params(CoreModel):
    brightness: float = Field(
        default=1, description="Brightness adjustment factor (e.g., 1.0 for no change)"
    )
    contrast: float = Field(
        default=1, description="Contrast adjustment factor (e.g., 1.0 for no change)"
    )


@func.set_output
class Outputs(CoreModel):
    adjusted_image: Image = Field(
        ..., description="Image with adjusted brightness and contrast"
    )
