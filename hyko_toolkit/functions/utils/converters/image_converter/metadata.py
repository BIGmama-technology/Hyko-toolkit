from enum import Enum

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel


class SupportedTypes(str, Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    tiff = "tiff"
    tif = "tif"
    bmp = "bmp"
    webp = "webp"
    jp2 = "jp2"
    dib = "dib"
    pgm = "pgm"
    ppm = "ppm"
    pnm = "pnm"
    ras = "ras"
    hdr = "hdr"


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
