from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.API,
    name="groq_chat_api",
    task="groq",
    description="Use Groq api for text generation.",
    cost=138,
)


class Model(str, Enum):
    mixtral8x7b = "mixtral-8x7b-32768"
    llama270b = "llama2-70b-4096"
    gemma7bit = "gemma-7b-it"


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
        default=Model.mixtral8x7b,
        description="Groq model to use.",
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
        component=Slider(leq=2, geq=0, step=0.1),
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="generated text.")


class Message(CoreModel):
    content: str


class Choice(CoreModel):
    message: Message


class GroqResponse(CoreModel):
    model: str
    choices: list[Choice]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {params.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "messages": [
                    {"role": "system", "content": inputs.system_prompt},
                    {"role": "user", "content": inputs.prompt},
                ],
                "model": params.model.value,
                "temperature": params.temperature,
                "max_tokens": params.max_tokens,
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = GroqResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.choices[0].message.content)
