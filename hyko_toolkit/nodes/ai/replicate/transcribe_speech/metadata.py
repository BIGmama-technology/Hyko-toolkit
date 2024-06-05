import asyncio
import base64
import time
from enum import Enum

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

func = ToolkitNode(
    name="Replicate transcribe speech",
    cost=3,
    description="Transcribe audio to text in multiple languages.",
    icon="replicate",
)


class Model(str, Enum):
    incredibly_fast_whisper = "vaibhavs10/incredibly-fast-whisper"
    whisper = "openai/whisper"


@func.set_input
class Inputs(CoreModel):
    audio: Audio = field(description="Input Audio.")


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.incredibly_fast_whisper,
        description="Transcription model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="Generated text.")


class URLs(CoreModel):
    cancel: str
    get: str


class PredictionResponse(CoreModel):
    urls: URLs


class WOutput(CoreModel):
    transcription: str


class WTranscriptionResponse(CoreModel):
    output: WOutput


class FOutput(CoreModel):
    text: str


class FTranscriptionResponse(CoreModel):
    output: FOutput


@func.on_call
async def call(inputs: Inputs, params: Params):
    versions = {
        "incredibly_fast_whisper": "3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
        "whisper": "4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
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
                    "audio": "data:audio/wav;base64,"
                    + base64.b64encode(await inputs.audio.get_data()).decode("utf-8"),
                },
            },
            timeout=60 * 10,
        )
    if res1.is_success:
        url_response = PredictionResponse(**res1.json())
        start_time = time.time()
        while True:
            async with httpx.AsyncClient() as client:
                res2 = await client.request(
                    method=Method.get,
                    url=url_response.urls.get,
                    headers={"Authorization": "Bearer " + params.api_key},
                    timeout=60,
                )
            if res2.is_success:
                if "output" in res2.json():
                    if params.model.name == "whisper":
                        text = WTranscriptionResponse(**res2.json())
                        return Outputs(result=text.output.transcription)
                    else:
                        text = FTranscriptionResponse(**res2.json())
                        return Outputs(result=text.output.text)
            elif time.time() - start_time >= 600:
                raise TimeoutError("Timed out waiting for the output to be ready")
            await asyncio.sleep(5)
    else:
        raise APICallError(status=res1.status_code, detail=res1.text)
