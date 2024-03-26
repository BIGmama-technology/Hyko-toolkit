import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="google_search",
    task="google",
    description="Use Google API for Search.",
)


@func.set_input
class Inputs(CoreModel):
    query: str = Field(
        ...,
        description="The search query.",
    )


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    cse_id: str = Field(description="Search Engine ID")
    max_results: int = Field(
        default=5,
        description="Maximum number of results.",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="The concatenated results.")


class SearchResultItem(CoreModel):
    title: str
    link: str
    snippet: str


class GoogleSearchResponse(CoreModel):
    items: list[SearchResultItem]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.get,
            url="https://www.googleapis.com/customsearch/v1",
            params={
                "key": params.api_key,
                "cx": params.cse_id,
                "q": inputs.query,
                "num": params.max_results,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        result = GoogleSearchResponse(**res.json())
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=[item.link for item in result.items])
