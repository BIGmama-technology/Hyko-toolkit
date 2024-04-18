from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveFloat

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='resize_factor', task='image_utils', description='Resize an image by a factor', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/resize_factor')

class InterpolationMethod(str, Enum):
    Area = 'area'
    Linear = 'linear'
    Lanczos = 'lanczos'
    NearestNeighbor = 'nearest-neighbor'
    Cubic = 'cubic'

@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description='Input image to resize')

@func.set_param
class Params(CoreModel):
    scale_factor: PositiveFloat = Field(default=0, description='Scaling factor for resizing')
    interpolation: InterpolationMethod = Field(InterpolationMethod.Lanczos, description='Interpolation method for resizing')

@func.set_output
class Outputs(CoreModel):
    resized_image: Image = Field(..., description='Resized image')
