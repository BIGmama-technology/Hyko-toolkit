from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="get_dimensions",
    task="image_utils",
    description="Get the Height, Width, and number of Channels from an image",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image to get dimensions from")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    width: int = field(description="Width of the image")
    height: int = field(description="Height of the image")
    channels: int = field(description="Number of channels in the image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    image = await inputs.image.to_pil()
    width, height = image.size
    channels = len(image.getbands())
    return Outputs(width=width, height=height, channels=channels)
