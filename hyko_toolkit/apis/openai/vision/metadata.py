import base64

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="GPT4 vision",
    task="Openai",
    description="Use openai GPT4 api to understand images.",
    cost=600,
    icon="openai",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="The image to generate from.")
    system_prompt: str = field(
        default="You are a helpful assistant",
        description="generated text.",
        component=TextField(placeholder="Enter your system prompt here"),
    )
    prompt: str = field(
        description="The prompt to generate from.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
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


class Response(CoreModel):
    choices: list[Choice]


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
                "messages": [
                    {"role": "system", "content": inputs.system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{inputs.prompt}"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64.b64encode(await inputs.input_image.get_data()).decode('utf-8')}"
                                },
                            },
                        ],
                    },
                ],
                "max_tokens": params.max_tokens,
                "temperature": params.temperature,
                "model": "gpt-4-turbo",
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=response.choices[0].message.content)
