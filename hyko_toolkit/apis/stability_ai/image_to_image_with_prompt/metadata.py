import base64
from enum import Enum

import httpx
from hyko_sdk.components.components import Ext, Slider, TextField
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="image_to_image_with_prompt",
    task="stability_ai",
    description="Generate images from an existing image Using Stability.ai API .",
    cost=8,
)


@func.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="What you wish to see in the output image.",
        component=TextField(placeholder="Entre your prompt here"),
    )
    init_image: Image = field(
        description="Image used to initialize the diffusion process, in lieu of random noise.",
    )


class Model(str, Enum):
    STABLE_DIFFUSION_3 = "stable-diffusion-3"
    STABLE_DIFFUSION_2 = "stable-diffusion-2"


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.STABLE_DIFFUSION_3,
        description="Which Stability.ai model to use.",
    )
    negative_prompt: str = field(
        default="", description="What you do not wish to see in the output image.."
    )
    seed: int = field(default=0, description="Seed")
    image_strength: float = field(
        default=0.35,
        description="How much influence the init_image has on the diffusion process.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    result: Image = field(description="Generated Image.")


class Artifact(CoreModel):
    base64: str


class Response(CoreModel):
    artifacts: list[Artifact]


@func.on_call
async def call(inputs: Inputs, params: Params):
    urls = {
        "stable-diffusion-3": "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        "stable-diffusion-2": "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/image-to-image",
    }
    json_data = {
        "stable-diffusion-3": {
            "mode": "image-to-image",
            "prompt": inputs.prompt,
            "negative_prompt": params.negative_prompt,
            "seed": 0,
            "output_format": "png",
            "strength": params.image_strength,
        },
        "stable-diffusion-2": {
            "image_strength": params.image_strength,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": inputs.prompt,
            "cfg_scale": 7,
            "samples": 1,
            "steps": 30,
        },
    }
    files = {
        "stable-diffusion-3": {
            "image": (
                inputs.init_image.file_name,
                await inputs.init_image.get_data(),
                None,
            )
        },
        "stable-diffusion-2": {
            "init_image": (
                inputs.init_image.file_name,
                await inputs.init_image.get_data(),
                None,
            )
        },
    }
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=urls[params.model],
            headers={
                "authorization": f"Bearer {params.api_key}",
                "Accept": "application/json",
            },
            files=files[params.model],
            data=json_data[params.model],
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(**res.json())
        decoded_images = [
            base64.b64decode(image.base64) for image in response.artifacts
        ]
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(
        result=await Image(
            obj_ext=Ext.PNG,
        ).init_from_val(val=decoded_images[0])
    )
