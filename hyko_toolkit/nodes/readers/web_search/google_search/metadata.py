import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

node = ToolkitNode(
    name="Google search",
    description="Use Google API for Search.",
    cost=100,
    icon="google",
)


@node.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Enter your query here"),
    )


@node.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    cse_id: str = field(
        description="Search Engine ID",
        component=TextField(placeholder="CSE ID", secret=True),
    )
    max_results: int = field(
        default=5,
        description="Maximum number of results.",
    )


@node.set_output
class Outputs(CoreModel):
    result: list[str] = field(description="The concatenated results.")


class SearchResultItem(CoreModel):
    title: str
    link: str
    snippet: str


class GoogleSearchResponse(CoreModel):
    items: list[SearchResultItem]


@node.on_call
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
