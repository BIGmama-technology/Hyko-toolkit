from enum import Enum

import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="text_to_image",
    task="stability_ai",
    description="Use Stability.ai API for Image generation.",
)


class AspectRatio(str, Enum):
    RATIO_16_9 = "16:9"
    RATIO_1_1 = "1:1"
    RATIO_21_9 = "21:9"
    RATIO_2_3 = "2:3"
    RATIO_3_2 = "3:2"
    RATIO_4_5 = "4:5"
    RATIO_5_4 = "5:4"
    RATIO_9_16 = "9:16"
    RATIO_9_21 = "9:21"


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="What you wish to see in the output image.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    negative_prompt: str = Field(
        default="", description="What you do not wish to see in the output image.."
    )
    seed: int = Field(default=0, description="Seed")
    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.RATIO_1_1, description="Aspect Ratio"
    )


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
            url="https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={"authorization": f"Bearer {params.api_key}", "accept": "image/*"},
            files={"none": ""},
            data={
                "prompt": inputs.prompt,
                "negative_prompt": params.negative_prompt,
                "output_format": "png",
                "seed": params.seed,
                "aspect_ratio": params.aspect_ratio.value,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(image=res.content)
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    result = await Image(obj_ext=Ext.PNG).init_from_val(response.image)
    return Outputs(result=result)
