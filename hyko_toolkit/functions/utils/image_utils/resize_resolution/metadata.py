from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveInt

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='resize_resolution', task='image_utils', description='Resize an image to an exact resolution', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/resize_resolution')

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
    width: PositiveInt = Field(default=100, description='New width for the resized image')
    height: PositiveInt = Field(default=100, description='New height for the resized image')
    interpolation: InterpolationMethod = Field(default=InterpolationMethod.Lanczos, description='Interpolation method for resizing')

@func.set_output
class Outputs(CoreModel):
    resized_image: Image = Field(..., description='Resized image')
