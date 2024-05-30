from enum import Enum

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.API,
    name="Cohere text embedding",
    task="Cohere",
    cost=1,
    description="Use cohere api for text embedding.",
    icon="cohere",
)


class Model(str, Enum):
    embed_english = "embed-english-v3.0"
    embed_multilingual = "embed-multilingual-v3.0"


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text to embed.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    model: Model = field(
        default=Model.embed_multilingual.value,
        description="Cohere model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    embedding: list[float] = field(description="text embedding.")


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
