from enum import Enum

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="gemini_text_generation_api",
    task="gemini",
    description="Use gemini api for text generation.",
)


class Model(str, Enum):
    gemini_pro = "gemini-pro"
    gemini_1_pro_latest = "gemini-1.0-pro-latest"
    gemini_1_pro001 = "gemini-1.0-pro-001"


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="Input prompt.")


@func.set_param
class Params(CoreModel):
    model: Model = Field(
        default=Model.gemini_pro,
        description="Gemini model to use.",
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


class Part(CoreModel):
    text: str


class Content(CoreModel):
    parts: list[Part]


class Candidate(CoreModel):
    content: Content


class GeminiResponse(CoreModel):
    candidates: list[Candidate]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{params.model.value}:generateContent?key={params.api_key}",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "contents": [{"parts": [{"text": inputs.prompt}]}],
                "generationConfig": {
                    "temperature": params.temperature,
                    "maxOutputTokens": params.max_tokens,
                },
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = GeminiResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.candidates[0].content.parts[0].text)
