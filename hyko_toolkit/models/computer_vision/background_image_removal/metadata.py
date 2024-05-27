from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="Background image removal",
    task="Computer vision",
    cost=0,
    description="This function removes the background from the original input image.",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Original image")


@func.set_output
class Outputs(CoreModel):
    image: Image = field(description="Image without background")
