import base64

import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

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


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    image_strength: float = Field(
        default=0.35,
        description="How much influence the init_image has on the diffusion process.",
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
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.stability.ai/v1/generation/stable-diffusion-v1-6/image-to-image",
            headers={"authorization": f"Bearer {params.api_key}", "accept": "image/*"},
            files={"image": inputs.init_image.get_data()},
            data={
                "image_strength": params.image_strength,
                "init_image_mode": "IMAGE_STRENGTH",
                "text_prompts[0][text]": inputs.prompt,
                "cfg_scale": 7,
                "samples": 1,
                "steps": 30,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(**res.json())
        decoded_images = [
            base64.b64decode(image.base64) for image in response.artifacts
        ]
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=Image(val=decoded_images[0], obj_ext=Ext.PNG))
