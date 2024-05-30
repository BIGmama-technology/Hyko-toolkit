from enum import Enum

from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field
from PIL import Image as PILImage

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Padding",
    task="Image utils",
    category=Category.UTILS,
    cost=0,
    description="Adds padding to an image by a given amount from the left, right, top and bottom",
    icon="padding",
)


class FillColor(str, Enum):
    BLACK = "black"
    WHITE = "white"
    TRANSPARENT = "transparent"

    def get_color(self):
        """Select how to fill negative space that results from padding"""
        if self == FillColor.WHITE:
            fill_color = (255, 255, 255)
        elif self == FillColor.BLACK:
            fill_color = (0, 0, 0)
        else:
            fill_color = (0, 0, 0, 0)

        return fill_color


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image to be padded")


@func.set_param
class Params(CoreModel):
    right: int = field(default=10, description="Padding amount from the right")
    left: int = field(default=10, description="Padding amount from the left")
    top: int = field(default=10, description="Padding from the top")
    bottom: int = field(default=10, description="Padding from the bottom")
    negative_space_fill: FillColor = field(
        default=FillColor.WHITE, description="Fill color for padded area"
    )


@func.set_output
class Outputs(CoreModel):
    shifted_image: HykoImage = field(description="Padded image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    img = await inputs.image.to_pil()
    right_value = params.right
    left_value = params.left
    top_value = params.top
    bottom_value = params.bottom

    fill_color = params.negative_space_fill.get_color()
    new_width = img.width + right_value + left_value
    new_height = img.height + top_value + bottom_value

    padded_img = PILImage.new("RGBA", (new_width, new_height), fill_color)
    padded_img.paste(img, (left_value, top_value))
    shifted_image = await HykoImage.from_pil(padded_img)

    return Outputs(shifted_image=shifted_image)
