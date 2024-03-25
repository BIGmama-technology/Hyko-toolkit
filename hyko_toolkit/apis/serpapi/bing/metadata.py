import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="bing_search",
    task="serpapi",
    description="Use Bing API for Search.",
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
    country: str = Field(default="us", description="Country code")
    first: int = Field(
        default=1,
        description="Controls the offset of the organic results.",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="The concatenated results.")


class SearchResultItem(CoreModel):
    title: str
    link: str
    snippet: str


class BingSearchResponse(CoreModel):
    organic_results: list[SearchResultItem]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.get,
            url="https://serpapi.com/search",
            params={
                "api_key": params.api_key,
                "cc": params.country,
                "q": inputs.query,
                "first": params.first,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        result = BingSearchResponse(**res.json())

    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=[i.link for i in result.organic_results])
