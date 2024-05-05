import base64
from enum import Enum

import httpx
from hyko_sdk.components import Ext
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="image_to_image_with_prompt",
    task="stability_ai",
    description="Generate images from an existing image Using Stability.ai API .",
)


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="What you wish to see in the output image.")
    init_image: Image = Field(
        ...,
        description="Image used to initialize the diffusion process, in lieu of random noise.",
    )


class Model(str, Enum):
    STABLE_DIFFUSION_3 = "stable-diffusion-3"
    STABLE_DIFFUSION_2 = "stable-diffusion-2"


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    model: Model = Field(
        default=Model.STABLE_DIFFUSION_3,
        description="Which Stability.ai model to use.",
    )
    image_strength: float = Field(
        default=0.35,
        description="How much influence the init_image has on the diffusion process.",
    )
    negative_prompt: str = Field(
        default="", description="What you do not wish to see in the output image.."
    )
    seed: int = Field(default=0, description="Seed")


@func.set_output
class Outputs(CoreModel):
    result: Image = Field(..., description="Generated Image.")


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
            "model": "sd3",
            "seed": 0,
            "output_format": "png",
            "strength": params.image_strength,
        },
        "stable-diffusion-2": {
            "image_strength": params.image_strength,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": inputs.prompt,
            "negative_prompt": params.negative_prompt,
            "cfg_scale": 7,
            "samples": 1,
            "steps": 30,
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
            files={
                "init_image": (
                    inputs.init_image.file_name,
                    await inputs.init_image.get_data(),
                    None,
                )
            },
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
