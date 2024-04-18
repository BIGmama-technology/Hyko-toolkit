from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveInt

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='crop_edges', task='image_utils', description='Crop an image from the specified edges', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/image_utils/crop_edges')

@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description='Input image')

@func.set_param
class Params(CoreModel):
    top: PositiveInt = Field(default=0, description='Number of pixels to crop from the top')
    left: PositiveInt = Field(default=0, description='Number of pixels to crop from the left')
    right: PositiveInt = Field(default=0, description='Number of pixels to crop from the right')
    bottom: PositiveInt = Field(default=0, description='Number of pixels to crop from the bottom')

@func.set_output
class Outputs(CoreModel):
    cropped_image: Image = Field(..., description='Output cropped image')
