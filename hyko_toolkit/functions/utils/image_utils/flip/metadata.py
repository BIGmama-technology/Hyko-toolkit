from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='flip', task='image_utils', description='Flip an image based on the specified axis', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/flip')

class FlipAxis(str, Enum):
    horizontal = 'horizontal'
    vertical = 'vertical'
    both = 'both'

@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description='Input image')

@func.set_param
class Params(CoreModel):
    flip_axis: FlipAxis = Field(default=FlipAxis.horizontal, description='Flip axis: horizontal, vertical, both, or none')

@func.set_output
class Outputs(CoreModel):
    flipped_image: Image = Field(..., description='Output image')
