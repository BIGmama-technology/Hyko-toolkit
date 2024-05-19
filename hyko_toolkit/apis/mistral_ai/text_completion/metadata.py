from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="mistral_ai_text_completion",
    task="mistral_ai",
    description="Use mistral ai api for text completion.",
    cost=150,
)


class Model(str, Enum):
    OPEN_MISTRAL_7B = "open-mistral-7b"
    OPEN_MIXTRAL_8X7B = "open-mixtral-8x7b"
    MISTRAL_SMALL_LATEST = "mistral-small-latest"
    MISTRAL_MEDIUM_LATEST = "mistral-medium-latest"
    MISTRAL_LARGE_LATEST = "mistral-large-latest"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = field(
        default="You are a helpful assistant.",
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
        default=Model.MISTRAL_SMALL_LATEST,
        description="mistral ai model to use.",
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
    role: str
    content: str


class Choice(CoreModel):
    message: Message


class MistralResponse(CoreModel):
    choices: list[Choice]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.mistral.ai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {params.api_key}",
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
        response = MistralResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.choices[0].message.content)
