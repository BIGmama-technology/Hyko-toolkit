from enum import Enum

from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from PIL import Image
from pydantic import Field, PositiveInt

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="resize_resolution",
    task="image_utils",
    description="Resize an image to an exact resolution",
)


class InterpolationMethod(str, Enum):
    Area = "area"
    Linear = "linear"
    Lanczos = "lanczos"
    NearestNeighbor = "nearest-neighbor"
    Cubic = "cubic"


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = Field(..., description="Input image to resize")


@func.set_param
class Params(CoreModel):
    width: PositiveInt = Field(
        default=100, description="New width for the resized image"
    )
    height: PositiveInt = Field(
        default=100, description="New height for the resized image"
    )
    interpolation: InterpolationMethod = Field(
        default=InterpolationMethod.Lanczos,
        description="Interpolation method for resizing",
    )


@func.set_output
class Outputs(CoreModel):
    resized_image: HykoImage = Field(..., description="Resized image")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    pil_image = await inputs.image.to_pil()
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
    hyko_image = await HykoImage.from_pil(image_resized)

    return Outputs(resized_image=hyko_image)
