from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='brightness_and_contrast', task='image_utils', description='Adjust brightness and contrast of an image', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/brightness_and_contrast')

@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description='Input image to adjust brightness and contrast')

@func.set_param
class Params(CoreModel):
    brightness: float = Field(default=1, description='Brightness adjustment factor (e.g., 1.0 for no change)')
    contrast: float = Field(default=1, description='Contrast adjustment factor (e.g., 1.0 for no change)')

@func.set_output
class Outputs(CoreModel):
    adjusted_image: Image = Field(..., description='Image with adjusted brightness and contrast')
