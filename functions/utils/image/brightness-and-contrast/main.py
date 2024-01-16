import cv2
import numpy as np
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    img_np = inputs.image.to_ndarray()

    image_cv2 = cv2.cvtColor(np.array(img_np), cv2.COLOR_RGB2BGR)

    adjusted_image = cv2.convertScaleAbs(
        image_cv2, alpha=params.contrast, beta=params.brightness
    )
    adjusted_rgb_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)

    image = Image.from_ndarray(adjusted_rgb_image)

    return Outputs(adjusted_image=image)
