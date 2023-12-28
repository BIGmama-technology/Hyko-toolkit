import os

import cv2
import numpy as np
from fastapi import HTTPException
from PIL import Image as PIL_Image
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Remove a specified amount of pixels from all four borders of an image",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


class Params(CoreModel):
    amount: int = Field(
        ..., description="Number of pixels to drop from all four borders"
    )


class Outputs(CoreModel):
    cropped_image: Image = Field(..., description="Output image")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    file, ext = os.path.splitext(inputs.image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())

    image = PIL_Image.open(f"./image{ext}")

    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width, _ = image_cv2.shape

    if params.amount < 0:
        raise HTTPException(status_code=500, detail="Amount must not be less than 0")

    cropped_image = image_cv2[
        params.amount : height - params.amount, params.amount : width - params.amount
    ]

    if cropped_image.size == 0:
        raise HTTPException(
            status_code=500, detail="Cropped area resulted in an empty image"
        )

    cropped_rgb_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    cropped_image_output = Image.from_ndarray(cropped_rgb_image)

    return Outputs(cropped_image=cropped_image_output)
