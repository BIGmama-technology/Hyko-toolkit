import asyncio
import base64
import time
from enum import Enum

import httpx
from hyko_sdk.components.components import Ext, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

node = ToolkitNode(
    name="Replicate restore images",
    cost=3,
    description="These models restore and improve images by fixing defects like blur, noise, and low resolution.",
    icon="replicate",
)


class Model(str, Enum):
    bringing_old_photos_back_to_life = "microsoft/bringing-old-photos-back-to-life"
    swinir = "jingyunliang/swinir"
    ddcolor = "piddnad/ddcolor"


@node.set_input
class Inputs(CoreModel):
    image: Image = field(description="Input image.")


@node.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.ddcolor,
        description="Restoration model to use.",
    )


@node.set_output
class Outputs(CoreModel):
    result: Image = field(description="Restored image.")


class URLs(CoreModel):
    cancel: str
    get: str


class PredictionResponse(CoreModel):
    urls: URLs


class FOutput(CoreModel):
    output: str


class UpscaledImage(CoreModel):
    image: bytes


@node.on_call
async def call(inputs: Inputs, params: Params):
    versions = {
        "bringing_old_photos_back_to_life": "c75db81db6cbd809d93cc3b7e7a088a351a3349c9fa02b6d393e35e0d51ba799",
        "ddcolor": "ca494ba129e44e45f661d6ece83c4c98a9a7c774309beca01429b58fce8aa695",
        "swinir": "660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
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
                            url=output.output,
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
