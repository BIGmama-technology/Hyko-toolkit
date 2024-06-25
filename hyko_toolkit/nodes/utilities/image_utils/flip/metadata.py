from enum import Enum

from hyko_sdk.components.components import Ext
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from PIL import Image

node = ToolkitNode(
    name="Flip",
    cost=0,
    description="Flip an image based on the specified axis",
    icon="flip",
)


class FlipAxis(str, Enum):
    horizontal = "horizontal"
    vertical = "vertical"
    both = "both"


class SupportedTypes(Enum):
    png = Ext.PNG
    jpeg = Ext.JPEG
    bmp = Ext.BMP
    webp = Ext.WEBP


@node.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image")


@node.set_param
class Params(CoreModel):
    flip_axis: FlipAxis = field(
        default=FlipAxis.horizontal,
        description="Flip axis: horizontal, vertical, both, or none",
    )


@node.set_output
class Outputs(CoreModel):
    flipped_image: HykoImage = field(description="Output image")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    image = await inputs.image.to_pil()
    flip_axis = params.flip_axis
    if flip_axis == FlipAxis.horizontal:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif flip_axis == FlipAxis.vertical:
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif flip_axis == FlipAxis.both:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(
            Image.Transpose.FLIP_TOP_BOTTOM
        )
    flipped_image_output = await HykoImage.from_pil(image)
    return Outputs(flipped_image=flipped_image_output)
