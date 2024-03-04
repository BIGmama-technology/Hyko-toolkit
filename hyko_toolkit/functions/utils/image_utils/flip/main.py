import os

import cv2
import numpy as np
from fastapi.exceptions import HTTPException
from metadata import FlipAxis, Inputs, Outputs, Params, func
from PIL import Image as PIL_Image

from hyko_sdk.io import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())

    image = PIL_Image.open(f"./image{ext}")
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    flip_axis = params.flip_axis
    if flip_axis == FlipAxis.horizontal:
        flipped_image = cv2.flip(image_cv2, 1)
    elif flip_axis == FlipAxis.vertical:
        flipped_image = cv2.flip(image_cv2, 0)
    elif flip_axis == FlipAxis.both:
        flipped_image = cv2.flip(image_cv2, -1)
    else:
        raise HTTPException(status_code=500, detail="Invalid flip axis")

    flipped_rgb_image = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
    flipped_image_output = Image.from_ndarray(flipped_rgb_image)

    return Outputs(flipped_image=flipped_image_output)
