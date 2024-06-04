from fastapi import HTTPException
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field
from pydantic import PositiveInt

func = ToolkitNode(
    name="Crop border",
    task="Image utils",
    category=Category.UTILS,
    cost=0,
    description="Remove a specified amount of pixels from all four borders of an image",
    icon="crop",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image")


@func.set_param
class Params(CoreModel):
    cropped_width: PositiveInt = field(
        default=0, description="Number of pixels to drop from all four borders"
    )
    cropped_hight: PositiveInt = field(
        default=0, description="Number of pixels to drop from all four borders"
    )


@func.set_output
class Outputs(CoreModel):
    cropped_image: HykoImage = field(description="Output image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    pil_image = await inputs.image.to_pil()
    width, height = pil_image.size
    cropped_image = pil_image.crop(
        (
            params.cropped_width,
            params.cropped_hight,
            width - params.cropped_width,
            height - params.cropped_hight,
        )
    )
    if cropped_image.size == (0, 0):
        raise HTTPException(
            status_code=500, detail="Cropped area resulted in an empty image"
        )
    cropped_image_output = await HykoImage.from_pil(cropped_image)

    return Outputs(cropped_image=cropped_image_output)
