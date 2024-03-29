from enum import Enum

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="duckduckgo_search",
    task="serpapi",
    description="Use duckduckgo API for Search.",
)


class Region(str, Enum):
    ar_ar = "xr-ar"
    us_en = "us-en"
    uk_en = "uk-en"
    de_de = "de-de"
    fr_fr = "fr-fr"
    es_es = "es-es"
    it_it = "it-it"
    nl_nl = "nl-nl"
    jp_ja = "jp-ja"


@func.set_input
class Inputs(CoreModel):
    query: str = Field(
        ...,
        description="The search query.",
    )


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    region: Region = Field(
        default=Region.us_en,
        description="Defines the region to use for the DuckDuckGo search (default : us-en)",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="List of urls.")


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
                "kl": params.region.value,
                "q": inputs.query,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        result = BingSearchResponse(**res.json())

    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=[i.link for i in result.organic_results])
