from enum import Enum

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field
from PIL import Image
from pydantic import PositiveInt

func = ToolkitNode(
    name="Resize resolution",
    task="Image utils",
    category=Category.UTILS,
    cost=0,
    description="Resize an image to an exact resolution",
    icon="resize",
)


class InterpolationMethod(str, Enum):
    Area = "area"
    Linear = "linear"
    Lanczos = "lanczos"
    NearestNeighbor = "nearest-neighbor"
    Cubic = "cubic"


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(description="Input image to resize")


@func.set_param
class Params(CoreModel):
    width: PositiveInt = field(
        default=100, description="New width for the resized image"
    )
    height: PositiveInt = field(
        default=100, description="New height for the resized image"
    )
    interpolation: InterpolationMethod = field(
        default=InterpolationMethod.Lanczos,
        description="Interpolation method for resizing",
    )


@func.set_output
class Outputs(CoreModel):
    resized_image: HykoImage = field(description="Resized image")


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
