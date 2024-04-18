from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveInt

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='crop_border', task='image_utils', description='Remove a specified amount of pixels from all four borders of an image', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/crop_border')

@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description='Input image')

@func.set_param
class Params(CoreModel):
    cropped_width: PositiveInt = Field(default=0, description='Number of pixels to drop from all four borders')
    cropped_hight: PositiveInt = Field(default=0, description='Number of pixels to drop from all four borders')

@func.set_output
class Outputs(CoreModel):
    cropped_image: Image = Field(..., description='Output image')
