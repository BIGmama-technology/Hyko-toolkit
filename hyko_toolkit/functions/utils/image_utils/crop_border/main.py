import os

import cv2
import numpy as np
from fastapi import HTTPException
from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, func
from PIL import Image as PIL_Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.image.get_name())
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
