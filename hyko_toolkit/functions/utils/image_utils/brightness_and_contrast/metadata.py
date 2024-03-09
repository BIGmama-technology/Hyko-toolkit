from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
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
        ..., description="Brightness adjustment factor (e.g., 1.0 for no change)"
    )
    contrast: float = Field(
        ..., description="Contrast adjustment factor (e.g., 1.0 for no change)"
    )


@func.set_output
class Outputs(CoreModel):
    adjusted_image: Image = Field(
        ..., description="Image with adjusted brightness and contrast"
    )
