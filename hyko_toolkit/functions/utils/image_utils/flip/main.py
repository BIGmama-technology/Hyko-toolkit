from hyko_sdk.io import Image as HykoImage
from metadata import FlipAxis, Inputs, Outputs, Params, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    image = Image.fromarray(inputs.image.to_ndarray())  # type: ignore

    flip_axis = params.flip_axis
    if flip_axis == FlipAxis.horizontal:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_axis == FlipAxis.vertical:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    elif flip_axis == FlipAxis.both:
        image = image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)

    flipped_image_output = await HykoImage.from_pil(image)

    return Outputs(flipped_image=flipped_image_output)
