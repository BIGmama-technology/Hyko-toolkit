import base64

import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="gemini_vision_api",
    task="gemini",
    description="Use google gemini vision api to understand images.",
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
