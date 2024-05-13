from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="huggingface_chat_api",
    task="huggingface",
    description="Use huggingface api for text generation.",
)


class Model(str, Enum):
    NousHermes2Mixtral8x7B_DPO = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
    Mixtral8x7B_Instruct_v01 = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    Mistral7B_Instruct_v02 = "mistralai/Mistral-7B-Instruct-v0.2"
    zephyr7b_gemma_v01 = "HuggingFaceH4/zephyr-7b-gemma-v0.1"
    openchat3_5_0106 = "openchat/openchat-3.5-0106"
    gemma7b_it = "google/gemma-7b-it"
    gemma_2b = "google/gemma-2b"


@func.set_input
class Inputs(CoreModel):
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    model: Model = field(
        default=Model.Mistral7B_Instruct_v02,
        description="Huggingface model to use.",
    )
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    max_new_tokens: int = field(
        default=1024,
        description="The maximum number of tokens that can be generated in the chat completion.",
    )
    temperature: float = field(
        default=1.0,
        description="What sampling temperature to use, between 0 and 2, defaults to 1.",
        component=Slider(leq=0, geq=2, step=0.1),
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="generated text.")


class ResponseModel(CoreModel):
    generated_text: str


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://api-inference.huggingface.co/models/{params.model.value}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {params.api_key}",
            },
            json={
                "inputs": inputs.prompt,
                "temperature": params.temperature,
                "max_new_tokens": params.max_new_tokens,
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = ResponseModel(**res.json()[0])
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.generated_text)
