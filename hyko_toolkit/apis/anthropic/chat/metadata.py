from enum import Enum

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="anthropic_chat_api",
    task="anthropic",
    description="Use anthropic api for text generation.",
)


class Model(str, Enum):
    claude3_opus = "claude-3-opus-20240229"
    claude3_sonnet = "claude-3-sonnet-20240229"
    claude3_haiku = "claude-3-haiku-20240307"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = Field(
        default="You are a helpful assistant.", description="system prompt."
    )
    prompt: str = Field(..., description="Input prompt.")


@func.set_param
class Params(CoreModel):
    model: Model = Field(
        default=Model.claude3_opus,
        description="Cohere model to use.",
    )
    api_key: str = Field(description="API key")
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
