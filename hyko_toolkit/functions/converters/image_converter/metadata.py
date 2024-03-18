from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext
from pydantic import Field


class SupportedTypes(Enum):
    png = Ext.PNG
    jpeg = Ext.JPEG
    bmp = Ext.BMP
    webp = Ext.WEBP


func = ToolkitFunction(
    name="image_converter",
    task="converters",
    description="Convert an input image to a specified target image type.",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    target_type: SupportedTypes = Field(
        ...,
        description="The Target Type.",
    )


@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description="Converted image")
