from enum import Enum

import cv2
import numpy as np
from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Stack images horizontally or vertically",
    requires_gpu=False,
)


class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Inputs(CoreModel):
    image1: Image = Field(..., description="First image to stack")
    image2: Image = Field(..., description="Second image to stack")


class Params(CoreModel):
    orientation: Orientation = Field(
        ..., description="Stacking orientation (HORIZONTAL or VERTICAL)"
    )


class Outputs(CoreModel):
    stacked_image: Image = Field(..., description="Stacked image")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    image1 = inputs.image1.to_ndarray()
    image2 = inputs.image2.to_ndarray()
    orientation = params.orientation

    images = [image1, image2]

    max_h, max_w, max_c = 0, 0, 1
    for img in images:
        h, w, c = img.shape
        if c == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            c = 3
        max_h = max(h, max_h)
        max_w = max(w, max_w)
        max_c = max(c, max_c)

    fixed_images = []
    for img in images:
        h, w, c = img.shape

        fixed_img = img

        # fix images so they resize to the max image
        if orientation == Orientation.HORIZONTAL:
            if h < max_h:
                fixed_img = cv2.resize(
                    img,
                    (int(w * max_h / h), max_h),
                    interpolation=cv2.INTER_NEAREST,
                )
        elif orientation == Orientation.VERTICAL:
            if w < max_w:
                fixed_img = cv2.resize(
                    img,
                    (max_w, int(h * max_w / w)),
                    interpolation=cv2.INTER_NEAREST,
                )
        else:
            raise HTTPException(
                status_code=500, detail=f"Invalid orientation '{orientation}'"
            )

        # expand channel dims if necessary
        if c < max_c:
            temp_img = np.ones((max_h, max_w, max_c), dtype=np.float32)
            temp_img[:, :, :c] = fixed_img
            fixed_img = temp_img

        fixed_images.append(fixed_img.astype("float32"))

    if orientation == Orientation.HORIZONTAL:
        for i in range(len(fixed_images)):
            if fixed_images[i].shape[0] != fixed_images[0].shape[0]:
                raise HTTPException(
                    status_code=500,
                    detail="Inputted heights are not the same and could not be auto-fixed",
                )
            if fixed_images[i].dtype != fixed_images[0].dtype:
                raise HTTPException(
                    status_code=500,
                    detail="The image types are not the same and could not be auto-fixed",
                )
        image = Image.from_ndarray(cv2.hconcat(fixed_images).astype(np.uint8))

    elif orientation == Orientation.VERTICAL:
        for i in range(len(fixed_images)):
            if fixed_images[i].shape[1] != fixed_images[0].shape[1]:
                raise HTTPException(
                    status_code=500,
                    detail="Inputted widths are not the same and could not be auto-fixed",
                )

            if fixed_images[i].dtype != fixed_images[0].dtype:
                raise HTTPException(
                    status_code=500,
                    detail="The image types are not the same and could not be auto-fixed",
                )

        image = Image.from_ndarray(cv2.vconcat(fixed_images).astype(np.uint8))
    else:
        raise HTTPException(
            status_code=500, detail=f"Invalid orientation '{orientation}'"
        )

    return Outputs(stacked_image=image)
