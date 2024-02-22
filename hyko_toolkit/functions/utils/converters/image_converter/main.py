import os

import cv2
import numpy as np
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Convert an input image to a specified target image type.

    Parameters:
    - inputs (Inputs): An object containing the input image data.
    - params (Params): An object containing parameters including the target image type.

    Returns:
    - Outputs: An object containing the converted image data.
    """
    _, ext = os.path.splitext(inputs.input_image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.input_image.get_data())
    image = cv2.imread(f"./image{ext}")

    result_img_path = f"./image{ext.split('.')[-1]}.{params.target_type}"

    success = cv2.imwrite(
        result_img_path, cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    )
    if success:
        result = cv2.imread(result_img_path)
        return Outputs(image=Image.from_ndarray(result))
