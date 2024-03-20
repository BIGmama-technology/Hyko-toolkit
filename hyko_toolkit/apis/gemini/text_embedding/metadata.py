from enum import Enum

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="gemini_text_embedding",
    task="gemini",
    description="Use gemini api for text embedding.",
)


class Model(str, Enum):
    embedding001 = "models/embedding-001"


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to embed.")


@func.set_param
class Params(CoreModel):
    user_access_token: str = Field(description="API key")
    model: Model = Field(
        default=Model.embedding001.value,
        description="gemini model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    embedding: list[float] = Field(..., description="text embedding.")


class Embedding(CoreModel):
    values: list[float]


class GeminiResponse(CoreModel):
    embedding: Embedding


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://generativelanguage.googleapis.com/v1beta/{params.model}:embedContent?key={params.user_access_token}",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "model": params.model,
                "content": {"parts": [{"text": inputs.text}]},
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = GeminiResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(embedding=response.embedding.values)
