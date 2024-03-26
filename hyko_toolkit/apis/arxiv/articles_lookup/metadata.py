import re

import httpx
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="arxiv_articles_lookup",
    task="arxiv",
    description="Use Arxiv API for articles Search.",
)


@func.set_input
class Inputs(CoreModel):
    query: str = Field(
        ...,
        description="The search query.",
    )


@func.set_param
class Params(CoreModel):
    max_results: int = Field(
        default=5,
        description="Maximum number of search.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The concatenated titles and summaries.")


def extract(text: str):
    pattern = r"<title>(.*?)</title>\s*<summary>(.*?)</summary>"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n\n".join(
        [f"Title: {title}\nSummary: {summary}" for title, summary in matches]
    )


class ArxivPaper(CoreModel):
    text: str


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.get,
            url="http://export.arxiv.org/api/query",
            params={
                "search_query": f"all:{inputs.query}",
                "max_results": params.max_results,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = ArxivPaper(text=res.text)
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(result=extract(response.text))
