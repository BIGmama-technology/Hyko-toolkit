import base64

import openai
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = await openai.Image.acreate(
        prompt=inputs.prompt,
        api_key=params.api_key,
        response_format="b64_json",
        n=1,
        size="256x256",
    )

    img = base64.b64decode(res.get("data")[0]["b64_json"])
    img = Image(bytearray(img), filename="image.png", mime_type="PNG")
    return Outputs(generated_image=img)
