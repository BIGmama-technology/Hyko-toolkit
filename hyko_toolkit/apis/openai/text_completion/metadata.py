from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="openai_text_completion",
    task="openai",
    description="Use openai api for text completion.",
)


class Model(str, Enum):
    gpt_4 = "gpt-4"
    chatgpt = "gpt-3.5-turbo"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = field(
        default="You are a helpful assistant",
        description="generated text.",
        component=TextField(placeholder="Enter your system prompt here"),
    )
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.chatgpt,
        description="Openai model to use.",
    )
    max_tokens: int = field(
        default=1024,
        description="The maximum number of tokens that can be generated in the chat completion.",
    )
    temperature: float = field(
        default=1.0,
        description="What sampling temperature to use, between 0 and 2, defaults to 1.",
        component=Slider(leq=0, geq=2, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="generated text.")


class Message(CoreModel):
    role: str
    content: str


class Choice(CoreModel):
    index: int
    message: Message
    finish_reason: str


class Usage(CoreModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Response(CoreModel):
    created: int
    model: str
    choices: list[Choice]
    usage: Usage


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {params.api_key}",
            },
            json={
                "model": params.model,
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
        response = Response(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.choices[0].message.content)
