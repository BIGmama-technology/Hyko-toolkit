import os
from enum import Enum

import cv2
import numpy as np
from fastapi.exceptions import HTTPException
from PIL import Image as PIL_Image
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Flip an image based on the specified axis",
    requires_gpu=False,
)


class FlipAxis(str, Enum):
    horizontal = "horizontal"
    vertical = "vertical"
    both = "both"


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


class Params(CoreModel):
    flip_axis: FlipAxis = Field(
        ..., description="Flip axis: horizontal, vertical, both, or none"
    )


class Outputs(CoreModel):
    flipped_image: Image = Field(..., description="Output image")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    file, ext = os.path.splitext(inputs.image.get_name())  # type: ignore
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())  # type: ignore

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
