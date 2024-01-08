import base64

import openai
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="OpenAI Dalle 2 image generation model (API)",
    requires_gpu=False,
)


class Inputs(CoreModel):
    prompt: str = Field(..., description="User text prompt")


class Params(CoreModel):
    api_key: str = Field(..., description="OpenAI API KEY")


class Outputs(CoreModel):
    generated_image: Image = Field(
        ..., description="AI Generated image from user text prompt"
    )


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
