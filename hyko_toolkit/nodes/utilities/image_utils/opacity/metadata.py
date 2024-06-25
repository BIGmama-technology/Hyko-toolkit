from hyko_sdk.components.components import Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from PIL import Image
from pydantic import PositiveFloat

node = ToolkitNode(
    name="Opacity",
    cost=0,
    description="Adjusts the opacity of an image",
    icon="opacity",
)


@node.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image to adjust opacity")


@node.set_param
class Params(CoreModel):
    opacity: PositiveFloat = field(
        default=50,
        description="Opacity value (0-100)",
        component=Slider(leq=100, geq=0, step=1.0),
    )


@node.set_output
class Outputs(CoreModel):
    adjusted_image: HykoImage = field(description="Image with adjusted opacity")


@node.on_call
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
