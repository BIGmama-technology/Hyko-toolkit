import asyncio
import time
from enum import Enum

import httpx
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel, Ext, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="replicate_video_generation",
    task="replicate",
    description="Convert text prompts into video clips and animations.",
)


class Model(str, Enum):
    damo_text_to_video = "cjwbw/damo-text-to-video"
    zeroscope_v2_xl = "anotherjesse/zeroscope-v2-xl"


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="Input prompt.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    model: Model = Field(
        default=Model.damo_text_to_video,
        description="generation model to use.",
    )
    num_inference_steps: int = Field(
        default=50, description="Number of inference steps."
    )
    fps: int = Field(default=25, description="Frames per second.")
    seed: int = Field(default=0, description="Random seed.")


@func.set_output
class Outputs(CoreModel):
    result: Video = Field(..., description="Generated video.")


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


@func.on_call
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
