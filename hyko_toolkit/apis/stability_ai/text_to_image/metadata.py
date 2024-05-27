from enum import Enum

import httpx
from hyko_sdk.components.components import Ext, TextField
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Text to image",
    task="Stability ai",
    category=Category.API,
    description="Use Stability.ai API for Image generation.",
    cost=8,
    icon="stabilityai",
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


class Model(str, Enum):
    STABLE_DIFFUSION_3 = "stable-diffusion-3"
    STABLE_DIFFUSION_2 = "stable-diffusion-2"


@func.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="What you wish to see in the output image.",
        component=TextField(placeholder="Entre your prompt here"),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    negative_prompt: str = field(
        default="",
        description="What you do not wish to see in the output image.",
        component=TextField(placeholder="Entre the negative prompt here"),
    )
    model: Model = field(
        default=Model.STABLE_DIFFUSION_3,
        description="Which Stability.ai model to use.",
    )
    aspect_ratio: AspectRatio = field(
        default=AspectRatio.RATIO_1_1, description="Aspect Ratio"
    )
    seed: int = field(default=0, description="Seed")


@func.set_output
class Outputs(CoreModel):
    result: Image = field(description="Generated Image.")


class Response(CoreModel):
    image: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    urls = {
        "stable-diffusion-3": "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        "stable-diffusion-2": "https://api.stability.ai/v2beta/stable-image/generate/core",
    }
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=urls[params.model.value],
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
