from enum import Enum

import cv2
import numpy as np
from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Shift an image by a given amount in X and Y directions",
    requires_gpu=False,
)


class FillColor(Enum):
    AUTO = "auto"
    BLACK = "black"
    TRANSPARENT = "transparent"

    def get_color(self, channels: int):
        """Select how to fill negative space that results from shifting"""

        if self == FillColor.AUTO:
            fill_color = (0,) * channels
        elif self == FillColor.BLACK:
            fill_color = (0,) * channels if channels < 4 else (0, 0, 0, 1)
        else:
            fill_color = (0, 0, 0, 0)

        return fill_color


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be shifted")


class Params(CoreModel):
    amount_x: int = Field(..., description="Shift amount in the X direction")
    amount_y: int = Field(..., description="Shift amount in the Y direction")
    negative_space_fill: FillColor = Field(
        ..., description="Fill color for shifted area"
    )


class Outputs(CoreModel):
    shifted_image: Image = Field(..., description="Shifted image")


def get_h_w_c(image):
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    elif len(image.shape) == 3:
        height, width, channels = image.shape
    else:
        raise HTTPException(status_code=500, detail="Unsupported image shape")

    return height, width, channels


def convert_to_BGRA(img: np.ndarray, in_c: int) -> np.ndarray:
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
        image_cv2 = convert_to_BGRA(image_cv2, c)
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
