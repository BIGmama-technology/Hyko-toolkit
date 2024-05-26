from enum import Enum

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="Openai text embedding",
    task="Openai",
    description="Use openai api for text embedding.",
    cost=4,
    icon="openai",
)


class Model(str, Enum):
    ada_002 = "text-embedding-ada-002"
    large_3 = "text-embedding-3-large"
    small_3 = "text-embedding-3-small"


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
        default=Model.ada_002,
        description="Openai model to use.",
    )


@func.set_output
class Outputs(CoreModel):
    embedding: list[float] = field(description="text embedding.")


class Embedding(CoreModel):
    embedding: list[float]


class Usage(CoreModel):
    prompt_tokens: int
    total_tokens: int


class Response(CoreModel):
    data: list[Embedding]
    model: str
    usage: Usage


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.openai.com/v1/embeddings",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {params.api_key}",
            },
            json={
                "input": inputs.text,
                "model": params.model,
                "encoding_format": "float",
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(embedding=response.data[0].embedding)
