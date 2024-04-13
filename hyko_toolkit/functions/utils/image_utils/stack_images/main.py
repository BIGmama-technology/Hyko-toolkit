from hyko_sdk.io import Image as HykoImage
from metadata import Inputs, Orientation, Outputs, Params, func
from PIL import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    image1_pil = Image.fromarray(inputs.image1.to_ndarray())  # type: ignore
    image2_pil = Image.fromarray(inputs.image2.to_ndarray())  # type: ignore
    orientation = params.orientation

    if orientation == Orientation.HORIZONTAL:
        # Make images the same height
        max_height = max(image1_pil.height, image2_pil.height)
        image1_pil = image1_pil.resize(
            (int(image1_pil.width * max_height / image1_pil.height), max_height),
            resample=Image.Resampling.NEAREST,
        )
        image2_pil = image2_pil.resize(
            (int(image2_pil.width * max_height / image2_pil.height), max_height),
            resample=Image.Resampling.NEAREST,
        )
        combined_image = Image.new(
            "RGB", (image1_pil.width + image2_pil.width, max_height)
        )
        combined_image.paste(image1_pil, (0, 0))
        combined_image.paste(image2_pil, (image1_pil.width, 0))
    elif orientation == Orientation.VERTICAL:
        # Make images the same width
        max_width = max(image1_pil.width, image2_pil.width)
        image1_pil = image1_pil.resize(
            (max_width, int(image1_pil.height * max_width / image1_pil.width)),
            resample=Image.Resampling.NEAREST,
        )
        image2_pil = image2_pil.resize(
            (max_width, int(image2_pil.height * max_width / image2_pil.width)),
            resample=Image.Resampling.NEAREST,
        )
        combined_image = Image.new(
            "RGB", (max_width, image1_pil.height + image2_pil.height)
        )
        combined_image.paste(image1_pil, (0, 0))
        combined_image.paste(image2_pil, (0, image1_pil.height))
    else:
        combined_image = image1_pil

    stacked_image = await HykoImage.from_pil(combined_image)

    return Outputs(stacked_image=stacked_image)
