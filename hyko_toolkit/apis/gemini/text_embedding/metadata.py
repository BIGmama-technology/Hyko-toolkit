import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    category=Category.API,
    name="google_text_embedding",
    task="gemini",
    cost=1,
    description="Use google api for text embedding.",
)


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


@func.set_output
class Outputs(CoreModel):
    embedding: list[float] = field(description="text embedding.")


class Embedding(CoreModel):
    values: list[float]


class GoogleResponse(CoreModel):
    embedding: Embedding


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={params.api_key}",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "model": "models/embedding-001",
                "content": {"parts": [{"text": inputs.text}]},
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = GoogleResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(embedding=response.embedding.values)
