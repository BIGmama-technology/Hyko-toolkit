from hyko_sdk.io import Image as HykoImage
from metadata import Inputs, Outputs, Params, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    pil_image = Image.fromarray(await inputs.image.to_ndarray())
    rotated_image = pil_image.rotate(-params.rotation_angle, expand=True)
    rotated_image = await HykoImage.from_pil(rotated_image)

    return Outputs(rotated_image=rotated_image)
