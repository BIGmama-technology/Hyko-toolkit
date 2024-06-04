from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Tune studio text completion",
    task="Tune studio",
    category=Category.API,
    description="Use Tune Studio api for text completion.",
    cost=10,
    icon="tune",
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
    system_prompt: str = field(
        default="You are a helpful assistant",
        description="System prompt.",
        component=TextField(placeholder="Entre your system prompt here"),
    )
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Entre your prompt here"),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.Llama_3_8B,
        description="The selected model to use.",
    )
    max_tokens: int = field(
        default=1024,
        description="The maximum number of tokens that can be generated in the chat completion.",
    )
    temperature: float = field(
        default=1.0,
        description="What sampling temperature to use, between 0 and 2, defaults to 1.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="generated text.")


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
