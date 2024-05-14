from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="anthropic_chat_api",
    task="anthropic",
    description="Use anthropic api for text generation.",
    cost=600,
)


class Model(str, Enum):
    claude3_opus = "claude-3-opus-20240229"
    claude3_sonnet = "claude-3-sonnet-20240229"
    claude3_haiku = "claude-3-haiku-20240307"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = field(
        default="You are a helpful assistant.", description="system prompt."
    )
    prompt: str = field(
        description="Input prompt.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    model: Model = field(
        default=Model.claude3_opus,
        description="Cohere model to use.",
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


class Content(CoreModel):
    text: str


class AnthropicResponse(CoreModel):
    content: list[Content]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": f"{params.api_key}",
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": f"{params.model.value}",
                "system": f"{inputs.system_prompt}",
                "messages": [{"role": "user", "content": f"{inputs.prompt}"}],
                "temperature": params.temperature,
                "max_tokens": params.max_tokens,
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = AnthropicResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.content[0].text)
