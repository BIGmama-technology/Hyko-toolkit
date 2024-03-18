from metadata import Inputs, Outputs, Params, func
from PIL import Image, ImageEnhance

from hyko_sdk.io import Image as HykoImage


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    img_pil = Image.fromarray(inputs.image.to_ndarray())  # type: ignore

    # Adjusting brightness
    enhancer = ImageEnhance.Brightness(img_pil)
    img_pil_bright = enhancer.enhance(params.brightness)

    # Adjusting contrast
    enhancer = ImageEnhance.Contrast(img_pil_bright)
    img_pil_contrast = enhancer.enhance(params.contrast)

    image = HykoImage.from_pil(img_pil_contrast)

    return Outputs(adjusted_image=image)
