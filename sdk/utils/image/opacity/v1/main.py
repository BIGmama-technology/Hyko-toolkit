import os

import cv2
import numpy as np
from fastapi.exceptions import HTTPException
from metadata import Inputs, Outputs, Params, func
from PIL import Image as PIL_Image

from hyko_sdk.io import Image


def convert_to_bgra(image: np.ndarray, num_channels: int) -> np.ndarray:
    if num_channels == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    elif num_channels == 4:
        return image
    else:
        raise HTTPException(
            status_code=500,
            detail="Invalid number of input channels. Only 3 or 4 channels are supported.",
        )


def opacity(img: np.ndarray, opacity: float) -> np.ndarray:
    h, w, c = img.shape
    if opacity == 100 and c == 4:
        return img
    imgout = convert_to_bgra(img, c)
    opacity /= 100

    imgout[:, :, 3] *= opacity

    return imgout


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    file, ext = os.path.splitext(inputs.image.get_name())  # type: ignore
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())  # type: ignore

    img_np = np.array(PIL_Image.open(f"./image{ext}"))

    opacity = params.opacity
    if not (0 <= opacity <= 100):
        raise HTTPException(
            status_code=500, detail="Opacity must be a percentage between 0 and 100."
        )

    h, w, c = img_np.shape
    if opacity == 100 and c == 4:
        adjusted_img_np = img_np
    else:
        imgout = convert_to_bgra(img_np, c)
        opacity /= 100
        imgout[:, :, 3] = (imgout[:, :, 3] * opacity).astype(np.uint8)
        adjusted_img_np = imgout

    adjusted_image = Image.from_ndarray(adjusted_img_np)

    return Outputs(adjusted_image=adjusted_image)
