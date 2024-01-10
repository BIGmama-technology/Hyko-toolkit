import os

from metadata import Inputs, Outputs, Params, func
from PIL import Image as PIL_Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.image.get_name())  # type: ignore
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())  # type: ignore

    image = PIL_Image.open(f"./image{ext}")
    width, height = image.size
    channels = len(image.getbands())

    return Outputs(width=width, height=height, channels=channels)
