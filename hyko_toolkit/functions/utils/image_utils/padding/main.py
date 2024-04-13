import numpy as np
from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, func
from PIL import Image as PILImage


@func.on_execute
async def add_padding(inputs: Inputs, params: Params) -> Outputs:
    img = PILImage.fromarray(inputs.image.to_ndarray())  # type: ignore
    right_value = params.right
    left_value = params.left
    top_value = params.top
    bottom_value = params.bottom
    fill_color = params.negative_space_fill.get_color()
    new_width = img.width + right_value + left_value
    new_height = img.height + top_value + bottom_value
    padded_img = PILImage.new("RGBA", (new_width, new_height), fill_color)
    padded_img.paste(img, (left_value, top_value))

    shifted_image = await Image.from_ndarray(np.array(padded_img))

    return Outputs(shifted_image=shifted_image)
