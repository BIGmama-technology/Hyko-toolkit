import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

func = ToolkitNode(
    name="Mistral ai text embedding",
    description="Use mistral ai api for text embedding.",
    cost=1,
    icon="mistral",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Input text.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )


@func.set_output
class Outputs(CoreModel):
    result: list[float] = field(description="generated text.")


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
