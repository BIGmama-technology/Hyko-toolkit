from enum import Enum

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="tune_studio_text_completion",
    task="tune_studio",
    description="Use Tune Studio api for text completion.",
)


class Model(str, Enum):
    Llama_3_8B = "rohan/Meta-Llama-3-8B-Instruct"
    Llama_3_70B = "rohan/Meta-Llama-3-70B-Instruct"
    Tune_blob = "kaushikaakash04/tune-blob"
    Mixtral_x7b_inst_v01_32k = "rohan/mixtral-8x7b-inst-v0-1-32k"
    Openhermes_2_5_m7b_8k = "rohan/openhermes-2-5-m7b-8k"
    Tune_wizardlm_2_8x22b = "rohan/tune-wizardlm-2-8x22b"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = Field(
        default="You are a helpful assistant", description="system prompt."
    )
    prompt: str = Field(..., description="Input prompt.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    model: Model = Field(
        default=Model.Llama_3_8B,
        description="The selected model to use.",
    )
    max_tokens: int = Field(
        default=1024,
        description="The maximum number of tokens that can be generated in the chat completion.",
    )
    temperature: float = Field(
        default=1.0,
        description="What sampling temperature to use, between 0 and 2, defaults to 1.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="generated text.")


class Message(CoreModel):
    content: str


class Choices(CoreModel):
    message: Message


class ChatCompletionResponse(CoreModel):
    choices: list[Choices]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://proxy.tune.app/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": params.api_key,
            },
            json={
                "stream": False,
                "model": params.model.value,
                "max_tokens": params.max_tokens,
                "temperature": params.temperature,
                "messages": [
                    {"role": "system", "content": inputs.system_prompt},
                    {"role": "user", "content": inputs.prompt},
                ],
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = ChatCompletionResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.choices[0].message.content)
