import numpy as np
from hyko_sdk.io import Image as HykoImage
from metadata import Inputs, Outputs, Params, func
from PIL import Image, ImageEnhance


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    img_pil = Image.fromarray(inputs.image.to_ndarray())

    # Adjusting brightness
    enhancer = ImageEnhance.Brightness(img_pil)
    img_pil_bright = enhancer.enhance(params.brightness)

    # Adjusting contrast
    enhancer = ImageEnhance.Contrast(img_pil_bright)
    img_pil_contrast = enhancer.enhance(params.contrast)

    # Convert to ndarray for compatibility with hyko_sdk.io.Image
    img_np_final = np.array(img_pil_contrast)

    image = HykoImage.from_ndarray(img_np_final)

    return Outputs(adjusted_image=image)
