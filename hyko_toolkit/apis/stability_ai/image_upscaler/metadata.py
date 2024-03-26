from enum import Enum

import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="image_upscaler",
    task="stability_ai",
    description="Use Stability.ai API for Image upscaling.",
)


class OutputFormat(str, Enum):
    webp = "webp"
    jpeg = "jpeg"
    png = "png"


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="What you wish to see in the output image.")
    input_image: Image = Field(..., description="The image you wish to upscale.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    negative_prompt: str = Field(
        default="", description="What you do not wish to see in the output image."
    )
    creativity: float = Field(
        default=0,
        description="How creative the model should be when upscaling an image.",
    )
    output_format: OutputFormat = Field(
        default=OutputFormat.png, description="Output format"
    )
    seed: int = Field(default=0, description="Seed")


@func.set_output
class Outputs(CoreModel):
    result: Image = Field(..., description="Generated Image.")


class Response(CoreModel):
    image: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.stability.ai/v2beta/stable-image/upscale/creative",
            headers={"authorization": f"Bearer {params.api_key}", "accept": "image/*"},
            files={"image": inputs.input_image.get_data()},
            data={
                "prompt": inputs.prompt,
                "negative_prompt": params.negative_prompt,
                "output_format": params.output_format.value,
                "creativity": params.creativity,
                "seed": params.seed,
            },
            timeout=60 * 5,
        )
        if res.is_success:
            res_image = await client.request(
                method=Method.get,
                url=f"https://api.stability.ai/v2beta/stable-image/upscale/creative/result/{res.json().get('id')}",
                headers={
                    "authorization": f"Bearer {params.api_key}",
                    "accept": "image/*",
                },
                timeout=60 * 5,
            )
            if res_image.is_success:
                response = Response(image=res_image.content)
            else:
                raise APICallError(status=res_image.status_code, detail=res_image.text)
        else:
            raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=Image(val=response.image, obj_ext=Ext.PNG))
