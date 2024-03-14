import os
from io import BytesIO

from metadata import Inputs, Outputs, Params, func
from PIL import Image as PILImage

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
    image = PILImage.open(BytesIO(inputs.input_image.get_data()))

    image.save(f"converted-image.{params.target_type.name}")
    with open(f"converted-image.{params.target_type.name}", "rb") as file:
        val = file.read()

    os.remove(f"converted-image.{params.target_type.name}")

    return Outputs(image=Image(val=val, obj_ext=params.target_type.value))
