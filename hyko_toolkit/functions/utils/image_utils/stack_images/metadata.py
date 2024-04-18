from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='stack_images', task='image_utils', description='Stack images horizontally or vertically', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/stack_images')

class Orientation(str, Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

@func.set_input
class Inputs(CoreModel):
    image1: Image = Field(..., description='First image to stack')
    image2: Image = Field(..., description='Second image to stack')

@func.set_param
class Params(CoreModel):
    orientation: Orientation = Field(default=Orientation.HORIZONTAL, description='Stacking orientation (HORIZONTAL or VERTICAL)')

@func.set_output
class Outputs(CoreModel):
    stacked_image: Image = Field(..., description='Stacked image')
