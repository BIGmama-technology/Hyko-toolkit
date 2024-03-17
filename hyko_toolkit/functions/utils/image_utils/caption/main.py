import numpy as np
from metadata import CaptionColor, CaptionPosition, Inputs, Outputs, Params, func
from PIL import Image as PIL_Image
from PIL import ImageDraw, ImageFont

from hyko_sdk.io import Image


def add_caption(
    img: PIL_Image.Image,
    caption: str,
    size: int,
    position: CaptionPosition,
    color: CaptionColor,
) -> PIL_Image.Image:
    if color == CaptionColor.BLACK:
        font_color = (0, 0, 0)
    else:
        font_color = (255, 255, 255)

    text_position = (
        (10, 10) if position == CaptionPosition.TOP else (10, img.height - 10 - size)
    )

    font_path = "arial.ttf"
    font = ImageFont.truetype(font_path, size)
    draw = ImageDraw.Draw(img)
    draw.text(text_position, caption, font=font, fill=font_color)  # type: ignore

    return img


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    img_np = inputs.input_image.to_ndarray()
    img_pil = PIL_Image.fromarray(img_np)  # type: ignore

    caption = inputs.caption
    size = params.caption_size
    position = params.position
    color = params.caption_color

    captioned_img_pil = add_caption(img_pil, caption, size, position, color)

    captioned_image = Image.from_ndarray(np.array(captioned_img_pil))

    return Outputs(captioned_image=captioned_image)
