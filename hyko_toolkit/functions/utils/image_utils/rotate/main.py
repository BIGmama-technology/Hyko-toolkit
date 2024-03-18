from metadata import Inputs, Outputs, Params, func
from PIL import Image

from hyko_sdk.io import Image as HykoImage


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    pil_image = Image.fromarray(inputs.image.to_ndarray())  # type: ignore
    rotated_image = pil_image.rotate(-params.rotation_angle, expand=True)
    rotated_image = HykoImage.from_pil(rotated_image)

    return Outputs(rotated_image=rotated_image)
