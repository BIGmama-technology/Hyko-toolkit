import numpy as np
from fastapi.exceptions import HTTPException
from hyko_sdk.io import Image as HykoImage
from metadata import CaptionColor, CaptionPosition, Inputs, Outputs, Params, func
from PIL import Image, ImageDraw, ImageFont


def add_caption(
    img: Image.Image,
    caption: str,
    size: int,
    position: CaptionPosition,
    color: CaptionColor,
) -> Image.Image:
    draw = ImageDraw.Draw(img)

    font_size = int(size / 100 * 10)  # Adjust font size scale

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    _, text_height = draw.textsize(caption, font=font)  # type: ignore

    if position == CaptionPosition.TOP:
        caption_xy = (10, 10)
    elif position == CaptionPosition.BOTTOM:
        caption_xy = (10, img.height - text_height - 10)  # type: ignore
    else:
        raise HTTPException(
            status_code=500, detail="Caption position must be 'top' or 'bottom'"
        )

    draw.text(caption_xy, caption, fill=color.value)  # type: ignore

    return img


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    img_pil = Image.fromarray(inputs.input_image.to_ndarray())

    caption = params.caption
    size = params.caption_size
    position = params.position
    color = params.caption_color

    captioned_img_pil = add_caption(img_pil, caption, size, position, color)

    captioned_img_np = np.array(captioned_img_pil)

    captioned_image = HykoImage.from_ndarray(captioned_img_np)

    return Outputs(captioned_image=captioned_image)
