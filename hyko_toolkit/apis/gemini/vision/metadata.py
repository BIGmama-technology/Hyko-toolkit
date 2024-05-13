import base64

import httpx
from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="gemini_vision_api",
    task="gemini",
    description="Use google gemini vision api to understand images.",
)


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = field(
        default="You are a helpful assistant",
        description="generated text.",
        component=TextField(placeholder="Enter your system prompt here"),
    )
    prompt: str = field(
        description="The prompt to generate from.",
        component=TextField(placeholder="Enter your prompt here", multiline=True),
    )
    input_image: Image = field(description="The image to generate from.")


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
        component=Slider(leq=0, geq=2, step=0.1),
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="generated text.")


class Part(CoreModel):
    text: str


class Content(CoreModel):
    parts: list[Part]


class Candidate(CoreModel):
    content: Content


class GeminiVResponse(CoreModel):
    candidates: list[Candidate]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={params.api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": inputs.prompt},
                            {
                                "inlineData": {
                                    "mimeType": "image/png",
                                    "data": base64.b64encode(
                                        await inputs.input_image.get_data()
                                    ).decode("utf-8"),
                                }
                            },
                        ],
                    }
                ],
                "generationConfig": {
                    "temperature": params.temperature,
                    "maxOutputTokens": params.max_tokens,
                },
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = GeminiVResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=response.candidates[0].content.parts[0].text)
