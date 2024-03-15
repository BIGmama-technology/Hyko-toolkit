import os

import cv2
import numpy as np
from fastapi.exceptions import HTTPException
from hyko_sdk.io import Image
from metadata import CaptionColor, CaptionPosition, Inputs, Outputs, Params, func
from PIL import Image as PIL_Image


def add_caption(
    img: np.ndarray,
    caption: str,
    size: int,
    position: CaptionPosition,
    color: CaptionColor,
) -> np.ndarray:
    font = cv2.FONT_HERSHEY_SIMPLEX

    if size < 0:
        raise HTTPException(
            status_code=500, detail="Caption size must be a non-negative integer"
        )
    else:
        font_scale = size / 100
        font_thickness = 2

    if color == CaptionColor.BLACK:
        font_color = (0, 0, 0)
    elif color == CaptionColor.WHITE:
        font_color = (255, 255, 255)
    else:
        raise HTTPException(
            status_code=500, detail="Caption color must be 'black' or 'white'"
        )

    line_type = cv2.LINE_AA

    text_size = cv2.getTextSize(caption, font, font_scale, font_thickness)[0]
    text_width, text_height = text_size

    if position == CaptionPosition.TOP:
        caption_y = text_height + 10
    elif position == CaptionPosition.BOTTOM:
        caption_y = img.shape[0] - 10
    else:
        raise HTTPException(
            status_code=500, detail="Caption position must be 'top' or 'bottom'"
        )

    img = cv2.putText(
        img,
        caption,
        (10, caption_y),
        font,
        font_scale,
        font_color,
        font_thickness,
        line_type,
    )

    return img


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    file, ext = os.path.splitext(inputs.input_image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.input_image.get_data())

    img_np = np.array(PIL_Image.open(f"./image{ext}"))

    caption = params.caption
    size = params.caption_size
    position = params.position
    color = params.caption_color

    captioned_img_np = add_caption(img_np, caption, size, position, color)

    captioned_image = Image.from_ndarray(captioned_img_np)

    return Outputs(captioned_image=captioned_image)
