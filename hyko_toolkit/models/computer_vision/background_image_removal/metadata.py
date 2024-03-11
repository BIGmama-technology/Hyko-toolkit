from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="background_image_removal",
    task="computer_vision",
    description="This function removes the background from the original input image.",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Original image")


@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description="Image without background")
