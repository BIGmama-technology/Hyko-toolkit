from enum import Enum

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="cohere_text_embedding",
    task="cohere",
    description="Use cohere api for text embedding.",
)


class Model(str, Enum):
    embed_english = "embed-english-v3.0"
    embed_multilingual = "embed-multilingual-v3.0"


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to embed.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    model: Model = Field(
        default=Model.embed_multilingual.value,
        description="Cohere model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    embedding: list[float] = Field(..., description="text embedding.")


class EmbeddingsResponse(CoreModel):
    embeddings: list[list[float]]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.cohere.ai/v1/embed",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"bearer {params.api_key}",
            },
            json={
                "texts": [inputs.text],
                "model": params.model,
                "input_type": "search_document",
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = EmbeddingsResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(embedding=response.embeddings[0])
