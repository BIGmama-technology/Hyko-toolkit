from metadata import Inputs, Outputs, Params, func
from PIL import Image

from hyko_sdk.io import Image as HykoImage


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    pil_image = Image.fromarray(inputs.image.to_ndarray())  # type: ignore

    original_width, original_height = pil_image.size
    new_width = max(round(original_width * (params.scale_factor / 100)), 1)
    new_height = max(round(original_height * (params.scale_factor / 100)), 1)

    interpolation_methods = {
        "area": Image.Resampling.BOX,
        "linear": Image.Resampling.BILINEAR,
        "lanczos": Image.Resampling.LANCZOS,
        "nearest-neighbor": Image.Resampling.NEAREST,
        "cubic": Image.Resampling.BICUBIC,
    }

    interpolation = interpolation_methods.get(
        params.interpolation, Image.Resampling.BOX
    )

    resized_pil_image = pil_image.resize((new_width, new_height), interpolation)
    resized_image = HykoImage.from_pil(resized_pil_image)

    return Outputs(resized_image=resized_image)
