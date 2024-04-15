from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    image = Image.fromarray(await inputs.image.to_ndarray())
    width, height = image.size
    channels = len(image.getbands())

    return Outputs(width=width, height=height, channels=channels)
