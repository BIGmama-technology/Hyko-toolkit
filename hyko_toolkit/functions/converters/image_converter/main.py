import os

from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, func


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
    image = (await inputs.input_image,)

    image.save(f"converted-image.{params.target_type.name}")
    with open(f"converted-image.{params.target_type.name}", "rb") as file:
        val = file.read()

    os.remove(f"converted-image.{params.target_type.name}")

    return Outputs(
        image=await Image(
            obj_ext=params.target_type.value,
        ).init_from_val(
            val=val,
        )
    )
