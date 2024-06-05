from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Background image removal",
    cost=0,
    description="This function removes the background from the original input image.",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Original image")


@func.set_output
class Outputs(CoreModel):
    image: Image = field(description="Image without background")
