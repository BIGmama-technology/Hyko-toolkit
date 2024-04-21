import base64

import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="gpt4_vision",
    task="openai",
    description="Use openai GPT4 api to understand images.",
)


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = Field(
        default="You are a helpful assistant", description="generated text."
    )
    prompt: str = Field(..., description="The prompt to generate from.")
    input_image: Image = Field(..., description="The image to generate from.")


@func.set_param
class Params(CoreModel):
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
