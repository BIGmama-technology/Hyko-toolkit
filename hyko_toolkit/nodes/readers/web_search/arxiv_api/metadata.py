import re

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

node = ToolkitNode(
    name="Arxiv articles lookup",
    cost=1,
    description="Use Arxiv API for articles Search.",
    icon="arxiv",
)


@node.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Enter your query here"),
    )


@node.set_param
class Params(CoreModel):
    max_results: int = field(
        default=5,
        description="Maximum number of search.",
    )


@node.set_output
class Outputs(CoreModel):
    result: str = field(description="The concatenated titles and summaries.")


def extract(text: str):
    pattern = r"<title>(.*?)</title>\s*<summary>(.*?)</summary>"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n\n".join(
        [f"Title: {title}\nSummary: {summary}" for title, summary in matches]
    )


class ArxivPaper(CoreModel):
    text: str


@node.on_call
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
