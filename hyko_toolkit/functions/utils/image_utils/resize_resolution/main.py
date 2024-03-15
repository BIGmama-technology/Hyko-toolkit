from hyko_sdk.io import Image as HykoImage
from metadata import Inputs, Outputs, Params, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    pil_image = Image.fromarray(inputs.image.to_ndarray())

    resize_methods = {
        "area": Image.Resampling.LANCZOS,
        "linear": Image.Resampling.BILINEAR,
        "lanczos": Image.Resampling.LANCZOS,
        "nearest-neighbor": Image.Resampling.NEAREST,
        "cubic": Image.Resampling.BICUBIC,
    }
    interpolation = resize_methods.get(params.interpolation, Image.Resampling.LANCZOS)

    image_resized = pil_image.resize(
        (params.width, params.height), resample=interpolation
    )
    hyko_image = HykoImage.from_pil(image_resized)

    return Outputs(resized_image=hyko_image)
