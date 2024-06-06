from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Background image removal",
    cost=0,
    description="This function removes the background from the original input image.",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Original image")


@node.set_output
class Outputs(CoreModel):
    image: Image = field(description="Image without background")
