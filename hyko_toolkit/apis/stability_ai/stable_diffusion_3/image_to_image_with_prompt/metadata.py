import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="image_to_image_with_prompt",
    task="stability_ai",
    description="Generate images from an existing image Using Stable Diffusion 3.0 Stability.ai API .",
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
    negative_prompt: str = Field(
        default="", description="What you do not wish to see in the output image.."
    )
    image_strength: float = Field(
        default=0.75,
        description="How much influence the init_image has on the diffusion process.",
    )
    seed: int = Field(default=0, description="Seed")


@func.set_output
class Outputs(CoreModel):
    result: Image = Field(..., description="Generated Image.")


class Response(CoreModel):
    data: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.stability.ai/v1/generation/stable-diffusion-v1-6/image-to-image",
            headers={
                "authorization": f"Bearer {params.api_key}",
                "Accept": "application/json",
            },
            files={
                "image": (
                    inputs.init_image.file_name,
                    await inputs.init_image.get_data(),
                    None,
                )
            },
            data={
                "mode": "image-to-image",
                "prompt": inputs.prompt,
                "negative_prompt": params.negative_prompt,
                "model": "sd3",
                "seed": 0,
                "output_format": "png",
                "strength": params.image_strength,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(data=res.content)
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(
        result=await Image(
            obj_ext=Ext.PNG,
        ).init_from_val(val=response.data)
    )
