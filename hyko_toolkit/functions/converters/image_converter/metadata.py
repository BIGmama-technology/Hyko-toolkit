from enum import Enum

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel
from hyko_sdk.types import Ext


class SupportedTypes(Enum):
    png = Ext.PNG
    jpeg = Ext.JPEG
    tiff = Ext.TIFF
    bmp = Ext.BMP
    jp2 = Ext.JP2
    ppm = Ext.PPM
    pnm = Ext.PNM
    ras = Ext.RAS
    hdr = Ext.HDR
    webp = Ext.WEBP


func = SDKFunction(
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
