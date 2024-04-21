from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from PIL import ImageEnhance
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="brightness_and_contrast",
    task="image_utils",
    description="Adjust brightness and contrast of an image",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = Field(
        ..., description="Input image to adjust brightness and contrast"
    )


@func.set_param
class Params(CoreModel):
    brightness: float = Field(
        default=1, description="Brightness adjustment factor (e.g., 1.0 for no change)"
    )
    contrast: float = Field(
        default=1, description="Contrast adjustment factor (e.g., 1.0 for no change)"
    )


@func.set_output
class Outputs(CoreModel):
    adjusted_image: HykoImage = Field(
        ..., description="Image with adjusted brightness and contrast"
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    img_pil = await inputs.image.to_pil()
    # Adjusting brightness
    enhancer = ImageEnhance.Brightness(img_pil)
    img_pil_bright = enhancer.enhance(params.brightness)
    # Adjusting contrast
    enhancer = ImageEnhance.Contrast(img_pil_bright)
    img_pil_contrast = enhancer.enhance(params.contrast)
    image = await HykoImage.from_pil(img_pil_contrast)
    return Outputs(adjusted_image=image)
