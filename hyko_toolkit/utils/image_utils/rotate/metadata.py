from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import Toolkit

func = Toolkit(
    category=Category.UTILS,
    name="rotate",
    task="image_utils",
    cost=0,
    description="Rotate an image by a given angle",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image to be rotated")


@func.set_param
class Params(CoreModel):
    rotation_angle: int = field(default=30, description="Rotation angle in degrees")


@func.set_output
class Outputs(CoreModel):
    rotated_image: HykoImage = field(description="Rotated image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    pil_image = await inputs.image.to_pil()
    rotated_image = pil_image.rotate(-params.rotation_angle, expand=True)

    hyko_image = await HykoImage.from_pil(rotated_image)

    return Outputs(rotated_image=hyko_image)
