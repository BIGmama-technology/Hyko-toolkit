import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="cohere_chat_api",
    task="cohere",
    description="Use cohere api for text generation.",
)


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = Field(
        default="You are a helpful assistant", description="system prompt."
    )
    prompt: str = Field(..., description="Input prompt.")


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


class ChatHistoryItem(CoreModel):
    role: str
    message: str


class CohereResponse(CoreModel):
    text: str
    chat_history: list[ChatHistoryItem]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.cohere.ai/v1/chat",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"bearer {params.api_key}",
            },
            json={
                "chat_history": [
                    {"role": "SYSTEM", "message": inputs.system_prompt},
                ],
                "model": "command",
                "message": inputs.prompt,
                "temperature": params.temperature,
            },
            timeout=60 * 10,
        )
    if res.is_success:
        response = CohereResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=response.chat_history[-1].message)
