from enum import Enum

from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel, Ext
from PIL import Image
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="flip",
    task="image_utils",
    description="Flip an image based on the specified axis",
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


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    flip_axis: FlipAxis = Field(
        default=FlipAxis.horizontal,
        description="Flip axis: horizontal, vertical, both, or none",
    )


@func.set_output
class Outputs(CoreModel):
    flipped_image: HykoImage = Field(..., description="Output image")


@func.on_call
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
