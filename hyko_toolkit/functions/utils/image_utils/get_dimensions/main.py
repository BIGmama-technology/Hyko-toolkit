import os

from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, func
from PIL import Image as PIL_Image


@func.on_execute
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    _, ext = os.path.splitext(inputs.image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())

    image = PIL_Image.open(f"./image{ext}")
    width, height = image.size
    channels = len(image.getbands())

    return Outputs(width=width, height=height, channels=channels)
