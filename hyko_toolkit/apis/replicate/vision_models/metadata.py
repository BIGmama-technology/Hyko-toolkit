import asyncio
import base64
import time
from enum import Enum

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="replicate_vision_models",
    task="replicate",
    description="Vision models process and interpret visual information from images and videos.",
)


class Model(str, Enum):
    llava_13b = "yorickvp/llava-13b"
    moondream2 = "lucataco/moondream2"


@func.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="The prompt to be used for the model.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )
    image: Image = field(description="Input image.")


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.llava_13b,
        description="vision model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="generated text.")


class URLs(CoreModel):
    cancel: str
    get: str


class PredictionResponse(CoreModel):
    urls: URLs


class FOutput(CoreModel):
    output: list[str]


@func.on_call
async def call(inputs: Inputs, params: Params):
    versions = {
        "llava_13b": "b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
        "moondream2": "392a53ac3f36d630d2d07ce0e78142acaccc338d6caeeb8ca552fe5baca2781e",
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
                    return Outputs(result=" ".join(output.output))
            elif time.time() - start_time >= 600:
                raise TimeoutError("Timed out waiting for the output to be ready")
            await asyncio.sleep(5)
    else:
        raise APICallError(status=res1.status_code, detail=res1.text)
