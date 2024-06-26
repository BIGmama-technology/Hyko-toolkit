import httpx
from hyko_sdk.components.components import Ext, Slider, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

node = ToolkitNode(
    name="Image upscaler",
    description="Use Stability.ai API for Image upscaling.",
    cost=3,
    icon="stabilityai",
)


@node.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="What you wish to see in the output image.",
        component=TextField(placeholder="Entre your prompt here"),
    )
    input_image: Image = field(description="The image you wish to upscale.")


@node.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API KEY", component=TextField(placeholder="API KEY", secret=True)
    )
    negative_prompt: str = field(
        default="", description="What you do not wish to see in the output image."
    )
    seed: int = field(default=0, description="Seed")
    creativity: float = field(
        default=0.3,
        description="How creative the model should be when upscaling an image.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@node.set_output
class Outputs(CoreModel):
    result: Image = field(description="Generated Image.")


class Response(CoreModel):
    image: bytes


@node.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.stability.ai/v2beta/stable-image/upscale/creative",
            headers={"authorization": f"Bearer {params.api_key}", "accept": "image/*"},
            files={
                "image": (
                    inputs.input_image.file_name,
                    await inputs.input_image.get_data(),
                    None,
                )
            },
            data={
                "prompt": inputs.prompt,
                "negative_prompt": params.negative_prompt,
                "output_format": "png",
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
    return Outputs(
        result=await Image(
            obj_ext=Ext.PNG,
        ).init_from_val(
            val=response.image,
        )
    )
