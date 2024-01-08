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
    description="Resize an image by a factor",
    requires_gpu=False,
)


class InterpolationMethod(str, Enum):
    Area = "area"
    Linear = "linear"
    Lanczos = "lanczos"
    NearestNeighbor = "nearest-neighbor"
    Cubic = "cubic"


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to resize")


class Params(CoreModel):
    scale_factor: float = Field(..., description="Scaling factor for resizing")
    interpolation: InterpolationMethod = Field(
        ..., description="Interpolation method for resizing"
    )


class Outputs(CoreModel):
    resized_image: Image = Field(..., description="Resized image")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if params.scale_factor <= 0:
        raise HTTPException(
            status_code=500, detail="Scale factor must be a positive value"
        )

    file, ext = os.path.splitext(inputs.image.get_name())  # type: ignore
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())  # type: ignore

    image_pil = PIL_Image.open(f"./image{ext}")
    image_cv2 = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    interpolation_methods = {
        "area": cv2.INTER_AREA,
        "linear": cv2.INTER_LINEAR,
        "lanczos": cv2.INTER_LANCZOS4,
        "nearest-neighbor": cv2.INTER_NEAREST,
        "cubic": cv2.INTER_CUBIC,
    }
    interpolation = interpolation_methods.get(params.interpolation, cv2.INTER_AREA)

    h, w, _ = image_cv2.shape
    out_dims = (
        max(round(w * (params.scale_factor / 100)), 1),
        max(round(h * (params.scale_factor / 100)), 1),
    )

    resized_image_cv2 = cv2.resize(image_cv2, out_dims, interpolation=interpolation)
    resized_image = cv2.cvtColor(resized_image_cv2, cv2.COLOR_BGR2RGB)

    image_resized = Image.from_ndarray(resized_image)

    return Outputs(resized_image=image_resized)
