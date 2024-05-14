from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="openrouter_chat_api",
    task="openrouter",
    description="Use OpenRouter api for text generation.",
    cost=54,
)


class Model(str, Enum):
    nous_hermes_2_mixtral_8x7b_dpo = "nousresearch/nous-hermes-2-mixtral-8x7b-dpo"
    noromaid_mixtral_8x7b_instruct = "neversleep/noromaid-mixtral-8x7b-instruct"
    nous_capybara_7b = "nousresearch/nous-capybara-7b:free"
    mistral_7b_instruct = "mistralai/mistral-7b-instruct:free"
    mythomist_7b = "gryphe/mythomist-7b:free"
    toppy_m_7b = "undi95/toppy-m-7b:free"
    cinematika_7b = "openrouter/cinematika-7b:free"
    gemma_7b_it = "google/gemma-7b-it:free"
    openchat_7b = "openchat/openchat-7b:free"
    zephyr_7b_beta = "huggingfaceh4/zephyr-7b-beta:free"
    bagel_34b = "jondurbin/bagel-34b"
    llama_2_13b_chat = "meta-llama/llama-2-13b-chat"
    psyfighter_13b = "jebcarter/psyfighter-13b"
    psyfighter_13b_2 = "koboldai/psyfighter-13b-2"
    nous_hermes_llama2_13b = "nousresearch/nous-hermes-llama2-13b"
    codellama_34b_instruct = "meta-llama/codellama-34b-instruct"
    phind_codellama_34b = "phind/phind-codellama-34b"
    neural_chat_7b = "intel/neural-chat-7b"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = field(
        default="You are a helpful assistant",
        description="system prompt.",
        component=TextField(placeholder="Enter your system prompt here"),
    )
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    model: Model = field(
        default=Model.nous_capybara_7b,
        description="openrouter model to use.",
    )
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    max_tokens: int = field(
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


class Message(CoreModel):
    content: str


class Choice(CoreModel):
    message: Message


class OpenrouterResponse(CoreModel):
    choices: list[Choice]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {params.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": params.model.value,
                "messages": [
                    {"role": "system", "content": inputs.system_prompt},
                    {"role": "user", "content": inputs.prompt},
                ],
                "temperature": params.temperature,
                "max_tokens": params.max_tokens,
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = OpenrouterResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.choices[0].message.content)
