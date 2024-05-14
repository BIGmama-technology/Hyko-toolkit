from enum import Enum

from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from PIL import Image

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="stack_images",
    task="image_utils",
    cost=0,
    description="Stack images horizontally or vertically",
)


class Orientation(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@func.set_input
class Inputs(CoreModel):
    image1: HykoImage = field(description="First image to stack")
    image2: HykoImage = field(description="Second image to stack")


@func.set_param
class Params(CoreModel):
    orientation: Orientation = field(
        default=Orientation.HORIZONTAL,
        description="Stacking orientation (HORIZONTAL or VERTICAL)",
    )


@func.set_output
class Outputs(CoreModel):
    stacked_image: HykoImage = field(description="Stacked image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    image1_pil = await inputs.image1.to_pil()
    image2_pil = await inputs.image2.to_pil()
    orientation = params.orientation
    if orientation == Orientation.HORIZONTAL:
        # Make images the same height
        max_height = max(image1_pil.height, image2_pil.height)
        image1_pil = image1_pil.resize(
            (int(image1_pil.width * max_height / image1_pil.height), max_height),
            resample=Image.Resampling.NEAREST,
        )
        image2_pil = image2_pil.resize(
            (int(image2_pil.width * max_height / image2_pil.height), max_height),
            resample=Image.Resampling.NEAREST,
        )
        combined_image = Image.new(
            "RGB", (image1_pil.width + image2_pil.width, max_height)
        )
        combined_image.paste(image1_pil, (0, 0))
        combined_image.paste(image2_pil, (image1_pil.width, 0))
    elif orientation == Orientation.VERTICAL:
        # Make images the same width
        max_width = max(image1_pil.width, image2_pil.width)
        image1_pil = image1_pil.resize(
            (max_width, int(image1_pil.height * max_width / image1_pil.width)),
            resample=Image.Resampling.NEAREST,
        )
        image2_pil = image2_pil.resize(
            (max_width, int(image2_pil.height * max_width / image2_pil.width)),
            resample=Image.Resampling.NEAREST,
        )
        combined_image = Image.new(
            "RGB", (max_width, image1_pil.height + image2_pil.height)
        )
        combined_image.paste(image1_pil, (0, 0))
        combined_image.paste(image2_pil, (0, image1_pil.height))
    else:
        combined_image = image1_pil

    stacked_image = await HykoImage.from_pil(combined_image)

    return Outputs(stacked_image=stacked_image)
