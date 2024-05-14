import asyncio
import base64
import time
from enum import Enum

import httpx
from hyko_sdk.components.components import Ext, TextField
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="replicate_upscale_images",
    task="replicate",
    cost=3,
    description="These models increase image resolution and quality.",
)


class Model(str, Enum):
    high_resolution_controlnet_til = "batouresearch/high-resolution-controlnet-tile"
    clarity_upscaler = "philz1337x/clarity-upscaler"


@func.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )
    image: Image = field(description="Input image.")


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.clarity_upscaler,
        description="upscaling model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    result: Image = field(description="upscaled image.")


class URLs(CoreModel):
    cancel: str
    get: str


class PredictionResponse(CoreModel):
    urls: URLs


class FOutput(CoreModel):
    output: list[str]


class UpscaledImage(CoreModel):
    image: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    versions = {
        "high_resolution_controlnet_til": "4af11083a13ebb9bf97a88d7906ef21cf79d1f2e5fa9d87b70739ce6b8113d29",
        "clarity_upscaler": "b8a46b09384dc1ac996596bc14058e2b7604971128ee7de709a40d4bbf982d2c",
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
                    "image": "data:image/jpeg;base64,"
                    + base64.b64encode(await inputs.image.get_data()).decode("utf-8"),
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
                    output = FOutput(**res2.json())
                    async with httpx.AsyncClient() as client:
                        res3 = await client.request(
                            method=Method.get,
                            url=output.output[0],
                            headers={"Authorization": "Bearer " + params.api_key},
                            timeout=60,
                        )
                        if res3.is_success:
                            fimg = UpscaledImage(image=res3.content)
                            result = await Image(obj_ext=Ext.PNG).init_from_val(
                                fimg.image
                            )
                            return Outputs(result=result)
            elif time.time() - start_time >= 600:
                raise TimeoutError("Timed out waiting for the output to be ready")
            await asyncio.sleep(5)
    else:
        raise APICallError(status=res1.status_code, detail=res1.text)
