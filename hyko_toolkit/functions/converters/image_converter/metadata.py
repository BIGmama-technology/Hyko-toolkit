from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction


class SupportedTypes(Enum):
    png = Ext.PNG
    jpeg = Ext.JPEG
    bmp = Ext.BMP
    webp = Ext.WEBP
func = ToolkitFunction(name='image_converter', task='converters', description='Convert an input image to a specified target image type.', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/converters/image_converter/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/converters/image_converter')

@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description='Input image')

@func.set_param
class Params(CoreModel):
    target_type: SupportedTypes = Field(..., description='The Target Type.')

@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description='Converted image')
