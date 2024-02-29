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
        "png": Ext.PNG,
        "jpeg": Ext.JPEG,
        "jpg": Ext.JPG,
        "tiff": Ext.TIFF,
        "tif": Ext.TIF,
        "bmp": Ext.BMP,
        "jp2": Ext.JP2,
        "dib": Ext.DIB,
        "ppm": Ext.PPM,
        "pnm": Ext.PNM,
        "ras": Ext.RAS,
        "hdr": Ext.HDR,
        "webp": Ext.WEBP,
    }
    image_np = np.frombuffer(inputs.input_image.get_data(), dtype=np.uint8)
    image = cv2.imdecode(image_np, flags=cv2.IMREAD_COLOR)
    success, encoded_image = cv2.imencode(f".{params.target_type.value}", image)
    target_buffer = encoded_image.tobytes()
    if success:
        return Outputs(
            image=Image(
                val=target_buffer, obj_ext=type_to_object[params.target_type.value]
            )
        )
