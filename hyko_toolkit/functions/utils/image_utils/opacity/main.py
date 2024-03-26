from hyko_sdk.io import Image as HykoImage
from metadata import Inputs, Outputs, Params, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    image = Image.fromarray(inputs.image.to_ndarray())  # type: ignore

    # Create an alpha layer with the same dimensions as the image, filled with the desired opacity
    alpha = Image.new("L", image.size, color=int(params.opacity * 255 / 100))
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Split the image into its components and combine them with the new alpha layer
    r, g, b, _ = image.split()
    image_with_opacity = Image.merge("RGBA", (r, g, b, alpha))

    adjusted_image_output = HykoImage.from_pil(image_with_opacity)

    return Outputs(adjusted_image=adjusted_image_output)
