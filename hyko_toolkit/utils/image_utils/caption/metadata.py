from enum import Enum

from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from PIL import ImageDraw, ImageFont
from pydantic import Field, PositiveInt

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="caption",
    task="image_utils",
    description="Add caption to an image",
)


class CaptionColor(str, Enum):
    WHITE = "white"
    BLACK = "black"


class CaptionPosition(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"


@func.set_input
class Inputs(CoreModel):
    input_image: HykoImage = Field(..., description="Input image to add a caption to")
    caption: str = Field(..., description="Caption text to be added")


@func.set_param
class Params(CoreModel):
    caption_size: PositiveInt = Field(default=12, description="Caption size in pixels")
    caption_color: CaptionColor = Field(
        default=CaptionColor.BLACK, description="Caption color: white or black"
    )
    position: CaptionPosition = Field(
        default=CaptionPosition.TOP, description="Position to add the caption"
    )


@func.set_output
class Outputs(CoreModel):
    captioned_image: HykoImage = Field(..., description="Image with added caption")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    img_pil = await inputs.input_image.to_pil()

    caption = inputs.caption
    size = params.caption_size
    position = params.position
    color = params.caption_color
    if color == CaptionColor.BLACK:
        font_color = (0, 0, 0)
    else:
        font_color = (255, 255, 255)
    text_position = (
        (10, 10)
        if position == CaptionPosition.TOP
        else (10, img_pil.height - 10 - size)
    )
    font_path = "arial.ttf"
    font = ImageFont.truetype(font_path, size)
    draw = ImageDraw.Draw(img_pil)
    draw.text(text_position, caption, font=font, fill=font_color)  # type: ignore
    captioned_image = await HykoImage.from_pil(img_pil)
    return Outputs(captioned_image=captioned_image)
