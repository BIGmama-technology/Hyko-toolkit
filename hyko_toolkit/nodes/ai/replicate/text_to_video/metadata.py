import asyncio
import time
from enum import Enum

import httpx
from hyko_sdk.components.components import Ext, Slider, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

node = ToolkitNode(
    name="Replicate video generation",
    cost=3,
    description="Convert text prompts into video clips and animations.",
    icon="replicate",
)


class Model(str, Enum):
    damo_text_to_video = "cjwbw/damo-text-to-video"
    zeroscope_v2_xl = "anotherjesse/zeroscope-v2-xl"


@node.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.damo_text_to_video,
        description="generation model to use.",
    )
    num_inference_steps: int = field(
        default=50,
        description="Number of inference steps.",
        component=Slider(leq=200, geq=10, step=10),
    )
    fps: int = field(
        default=25,
        description="Frames per second.",
        component=Slider(leq=100, geq=1, step=1),
    )
    seed: int = field(default=0, description="Random seed.")


@node.set_output
class Outputs(CoreModel):
    result: Video = field(description="Generated video.")


class URLs(CoreModel):
    cancel: str
    get: str


class PredictionResponse(CoreModel):
    urls: URLs


class ZOutput(CoreModel):
    output: list[str]


class DOutput(CoreModel):
    output: str


class GVedio(CoreModel):
    vedio: bytes


@node.on_call
async def call(inputs: Inputs, params: Params):
    versions = {
        "damo_text_to_video": "1e205ea73084bd17a0a3b43396e49ba0d6bc2e754e9283b2df49fad2dcf95755",
        "zeroscope_v2_xl": "9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
    }
    async with httpx.AsyncClient() as client:
        res1 = await client.request(
            method=Method.post,
            url="https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": "Bearer " + params.api_key,
                "Content-Type": "application/json",
            },
            json={
                "version": versions[params.model.name],
                "input": {
                    "prompt": inputs.prompt,
                    "number_of_inference_steps": params.num_inference_steps,
                    "fps": params.fps,
                    "seed": params.seed,
                },
            },
            timeout=60 * 10,
        )
    if res1.is_success:
        response = PredictionResponse(**res1.json())
        start_time = time.time()
        while True:
            async with httpx.AsyncClient() as client:
                res2 = await client.request(
                    method=Method.get,
                    url=response.urls.get,
                    headers={"Authorization": "Bearer " + params.api_key},
                    timeout=60,
                )
            if res2.is_success:
                if "output" in res2.json():
                    if params.model == Model.damo_text_to_video:
                        output = DOutput(**res2.json())
                        url = output.output
                    else:
                        output = ZOutput(**res2.json())
                        url = output.output[0]
                    async with httpx.AsyncClient() as client:
                        res3 = await client.request(
                            method=Method.get,
                            url=url,
                            headers={"Authorization": "Bearer " + params.api_key},
                            timeout=60,
                        )
                        if res3.is_success:
                            vid = GVedio(vedio=res3.content)
                            result = await Video(obj_ext=Ext.MP4).init_from_val(
                                vid.vedio
                            )
                            return Outputs(result=result)
            elif time.time() - start_time >= 600:
                raise TimeoutError("Timed out waiting for the output to be ready")
            await asyncio.sleep(5)
    else:
        raise APICallError(status=res1.status_code, detail=res1.text)
