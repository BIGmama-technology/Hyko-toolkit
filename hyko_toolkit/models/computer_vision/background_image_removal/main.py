from rembg import remove

from hyko_sdk.io import Image
from hyko_sdk.types import Ext

from .metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    This function removes the background from the original input image .

    Args:
        inputs (Inputs): An object containing the original input image data.
    Returns:
        Outputs: An object containing the processed image data without the background.
    """
    image_buffer = inputs.input_image.get_data()
    output = remove(image_buffer)
    return Outputs(image=Image(val=output, obj_ext=Ext.PNG))
