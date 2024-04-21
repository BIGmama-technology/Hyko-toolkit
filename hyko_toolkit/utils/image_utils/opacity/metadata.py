from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from PIL import Image
from pydantic import Field, PositiveFloat

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="opacity",
    task="image_utils",
    description="Adjusts the opacity of an image",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = Field(..., description="Input image to adjust opacity")


@func.set_param
class Params(CoreModel):
    opacity: PositiveFloat = Field(
        default=50, le=100, description="Opacity value (0-100)"
    )


@func.set_output
class Outputs(CoreModel):
    adjusted_image: HykoImage = Field(..., description="Image with adjusted opacity")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    image = await inputs.image.to_pil()
    # Create an alpha layer with the same dimensions as the image, filled with the desired opacity

    alpha = Image.new("L", image.size, color=int(params.opacity * 255 / 100))
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    # Split the image into its components and combine them with the new alpha layer
    r, g, b, _ = image.split()
    image_with_opacity = Image.merge("RGBA", (r, g, b, alpha))
    adjusted_image_output = await HykoImage.from_pil(image_with_opacity)
    return Outputs(adjusted_image=adjusted_image_output)
