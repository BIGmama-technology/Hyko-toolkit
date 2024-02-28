import os

import cv2
import numpy as np
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image
from hyko_sdk.types import Ext


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
    type_to_object = {
        "jpg": Ext.JPG,
        "tiff": Ext.TIFF,
        "tif": Ext.TIF,
        "bmp": Ext.BMP,
        "jp2": Ext.JP2,
        "dib": Ext.DIB,
        "pgm": Ext.PGM,
        "ppm": Ext.PPM,
        "pnm": Ext.PNM,
        "ras": Ext.RAS,
        "hdr": Ext.HDR,
    }
    image_np = np.frombuffer(inputs.input_image.get_data(), dtype=np.uint8)
    image = cv2.imdecode(image_np, flags=cv2.IMREAD_COLOR)
    _, ext = os.path.splitext(inputs.input_image.get_name())
    result_img_path = f"./image{ext.split('.')[-1]}.{params.target_type}"
    success = cv2.imwrite(
        result_img_path, cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    )
    if success:
        result = cv2.imread(result_img_path)
        return Outputs(
            image=Image.from_ndarray(
                result, encoding=type_to_object[params.target_type]
            )
        )
