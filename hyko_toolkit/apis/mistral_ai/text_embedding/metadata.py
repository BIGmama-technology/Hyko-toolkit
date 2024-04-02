import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="mistral_ai_text_embedding",
    task="mistral_ai",
    description="Use mistral ai api for text embedding.",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")


@func.set_output
class Outputs(CoreModel):
    result: list[float] = Field(..., description="generated text.")


class Embedding(CoreModel):
    embedding: list[float]


class EmbeddedData(CoreModel):
    data: list[Embedding]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.mistral.ai/v1/embeddings",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {params.api_key}",
            },
            json={
                "model": "mistral-embed",
                "input": [inputs.text],
                "encoding_format": "float",
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = EmbeddedData(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.data[0].embedding)
