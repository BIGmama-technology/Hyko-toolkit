import os

from PIL import Image as PIL_Image
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Get the Height, Width, and number of Channels from an image",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to get dimensions from")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    width: int = Field(..., description="Width of the image")
    height: int = Field(..., description="Height of the image")
    channels: int = Field(..., description="Number of channels in the image")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    file, ext = os.path.splitext(inputs.image.get_name())  # type: ignore
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())  # type: ignore

    image = PIL_Image.open(f"./image{ext}")
    width, height = image.size
    channels = len(image.getbands())

    return Outputs(width=width, height=height, channels=channels)
