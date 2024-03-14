import cv2
import numpy as np
from fastapi import HTTPException
from hyko_sdk.io import Image
from metadata import FillColor, Inputs, Outputs, Params, func


def get_h_w_c(image):
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    elif len(image.shape) == 3:
        height, width, channels = image.shape
    else:
        raise HTTPException(status_code=500, detail="Unsupported image shape")

    return height, width, channels


def convert_to_bgra(img: np.ndarray, in_c: int) -> np.ndarray:
    if in_c not in (1, 3, 4):
        raise HTTPException(
            status_code=500, detail=f"Number of channels ({in_c}) unexpected"
        )

    if in_c == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
    elif in_c == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    return img


@func.on_execute
async def shift_image(inputs: Inputs, params: Params) -> Outputs:
    img_np = inputs.image.to_ndarray()
    image_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    height, width, _ = image_cv2.shape

    amount_x = params.amount_x
    amount_y = params.amount_y
    fill = params.negative_space_fill

    c = get_h_w_c(image_cv2)[2]

    if fill == FillColor.TRANSPARENT:
        image_cv2 = convert_to_bgra(image_cv2, c)
    fill_color = fill.get_color(c)  # type: ignore

    translation_matrix = np.asfarray(
        [[1, 0, amount_x], [0, 1, amount_y]], dtype=np.float32
    )

    shifted_image = cv2.warpAffine(
        image_cv2,
        translation_matrix,
        (width, height),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=fill_color,
    )

    shifted_rgb_image = cv2.cvtColor(shifted_image, cv2.COLOR_BGRA2RGBA)

    shifted_image = Image.from_ndarray(shifted_rgb_image)

    return Outputs(shifted_image=shifted_image)
