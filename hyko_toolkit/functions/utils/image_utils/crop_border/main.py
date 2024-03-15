from fastapi import HTTPException
from hyko_sdk.io import Image as HykoImage
from metadata import Inputs, Outputs, Params, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    image = Image.fromarray(inputs.image.to_ndarray())

    width, height = image.size
    cropped_image = image.crop(
        (
            params.cropped_width,
            params.cropped_hight,
            width - params.cropped_width,
            height - params.cropped_hight,
        )
    )

    if cropped_image.size == (0, 0):
        raise HTTPException(
            status_code=500, detail="Cropped area resulted in an empty image"
        )

    cropped_image_output = HykoImage.from_pil(cropped_image)

    return Outputs(cropped_image=cropped_image_output)
