import httpx
from hyko_sdk.components.components import Ext, TextField
from hyko_sdk.io import Image, Video
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Image to video",
    task="Stability ai",
    category=Category.API,
    description="Use Stability.ai API for Video generation from an existing image.",
    cost=3,
    icon="stabilityai",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="The image to be used as the input.")


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    seed: int = field(default=0, description="Random seed.")


@func.set_output
class Outputs(CoreModel):
    result: Video = field(description="Generated video.")


class Response(CoreModel):
    video: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.stability.ai/v2beta/image-to-video",
            headers={"authorization": f"Bearer {params.api_key}"},
            files={
                "image": (
                    inputs.input_image.file_name,
                    await inputs.input_image.get_data(),
                    None,
                )
            },
            data={
                "seed": params.seed,
            },
            timeout=60 * 5,
        )
        if res.is_success:
            res_video = await client.request(
                method=Method.get,
                url=f"https://api.stability.ai/v2beta/image-to-video/result/{res.json().get('id')}",
                headers={
                    "authorization": f"Bearer {params.api_key}",
                    "accept": "video/*",
                },
                timeout=60 * 5,
            )
            if res_video.is_success:
                response = Response(video=res_video.content)
            else:
                raise APICallError(status=res_video.status_code, detail=res_video.text)
        else:
            raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=await Video(obj_ext=Ext.MP4).init_from_val(response.video))
