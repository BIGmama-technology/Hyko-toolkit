from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image as HykoImage
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from PIL import ImageEnhance

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="Brightness and contrast",
    task="Image utils",
    cost=0,
    description="Adjust brightness and contrast of an image",
    icon="image",
)


@func.set_input
class Inputs(CoreModel):
    image: HykoImage = field(
        description="Input image to adjust brightness and contrast"
    )


@func.set_param
class Params(CoreModel):
    brightness: float = field(
        default=1.0,
        description="Brightness adjustment factor (e.g., 1.0 for no change)",
        component=Slider(leq=3, geq=0, step=0.01),
    )
    contrast: float = field(
        default=1.0,
        description="Contrast adjustment factor (e.g., 1.0 for no change)",
        component=Slider(leq=3, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    adjusted_image: HykoImage = field(
        description="Image with adjusted brightness and contrast",
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
