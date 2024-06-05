from enum import Enum

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

func = ToolkitNode(
    name="Cohere chat api",
    cost=1,
    description="Use cohere api for text generation.",
    icon="cohere",
)


class Model(str, Enum):
    command = "command"
    command_r = "command-r"
    command_light = "command-light"
    command_light_nightly = "command-light-nightly"
    command_nightly = "command-nightly"
    command_r_plus = "command-r-plus"


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
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.command,
        description="The selected model to use.",
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


class ChatHistoryItem(CoreModel):
    role: str
    message: str


class CohereResponse(CoreModel):
    text: str
    chat_history: list[ChatHistoryItem]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.cohere.ai/v1/chat",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"bearer {params.api_key}",
            },
            json={
                "chat_history": [
                    {"role": "SYSTEM", "message": inputs.system_prompt},
                ],
                "model": params.model.value,
                "message": inputs.prompt,
                "temperature": params.temperature,
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = CohereResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.chat_history[-1].message)
