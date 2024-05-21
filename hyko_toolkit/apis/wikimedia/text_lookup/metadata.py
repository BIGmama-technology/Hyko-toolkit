from enum import Enum

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import Toolkit

func = Toolkit(
    category=Category.API,
    name="wikipedia_text_lookup",
    task="wikimedia",
    cost=1,
    description="Use WikiPedia API for Search.",
)


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


@func.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Entre your query here"),
    )


@func.set_param
class Params(CoreModel):
    max_results: int = field(
        default=5,
        description="Maximum number of search.",
    )
    language: SupportedLanguages = field(
        default=SupportedLanguages.english,
        description="The search Language.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="The concatenated titles and summaries.")


class QueryPage(CoreModel):
    title: str
    extract: str


class Query(CoreModel):
    pages: dict[str, QueryPage]


class WikipediaResult(CoreModel):
    query: Query


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.get,
            url=f"https://{params.language.value}.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": inputs.query,
                "gsrlimit": params.max_results,
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = WikipediaResult(**res.json())
        titles_list = [page_data.title for page_data in response.query.pages.values()]
        extract_list = [
            page_data.extract for page_data in response.query.pages.values()
        ]
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(
        result="\n\n".join(
            [
                f"Title: {title}\nText: {extract}"
                for title, extract in zip(titles_list, extract_list)
            ]
        )
    )
