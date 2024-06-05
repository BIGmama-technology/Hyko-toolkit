from fastapi import HTTPException
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from pydantic import PositiveInt

func = ToolkitNode(
    name="Crop edges",
    cost=0,
    description="Crop an image from the specified edges",
    icon="crop",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image")


@func.set_param
class Params(CoreModel):
    top: PositiveInt = field(
        default=0,
        description="Number of pixels to crop from the top",
    )
    left: PositiveInt = field(
        default=0,
        description="Number of pixels to crop from the left",
    )
    right: PositiveInt = field(
        default=0,
        description="Number of pixels to crop from the right",
    )
    bottom: PositiveInt = field(
        default=0,
        description="Number of pixels to crop from the bottom",
    )


@func.set_output
class Outputs(CoreModel):
    cropped_image: HykoImage = field(description="Output cropped image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    pil_image = await inputs.image.to_pil()
    width, height = pil_image.size
    cropped_image = pil_image.crop(
        (params.left, params.top, width - params.right, height - params.bottom)
    )
    if cropped_image.size == (0, 0):
        raise HTTPException(
            status_code=500, detail="Cropped area resulted in an empty image"
        )
    cropped_image_output = await HykoImage.from_pil(cropped_image)

    return Outputs(cropped_image=cropped_image_output)
