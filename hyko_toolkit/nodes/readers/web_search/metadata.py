from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .arxiv_api.metadata import func as arxiv_api_node
from .bing_serpapi.metadata import func as bing_serpapi_node
from .duckduckgo_search.metadata import func as duckduckgo_search_node
from .duckduckgo_serpapi.metadata import func as duckduckgo_serpapi_node
from .google_place.metadata import func as google_place_node
from .wikipedia_api.metadata import func as wikipedia_api_node
from .wikipedia_search.metadata import func as wikipedia_search_node

node = ToolkitNode(
    name="search_utils",
    description="perform various search and retrieval tasks.",
    tag=Tag.readers,
)


class SearchUtils(str, Enum):
    arxiv_api = "arxiv_api"
    bing_serpapi = "bing_serpapi"
    duckduckgo_search = "duckduckgo_search"
    duckduckgo_serpapi = "duckduckgo_serpapi"
    google_place = "google_place"
    wikipedia_api = "wikipedia_api"
    wikipedia_search = "wikipedia_search"


@node.set_param
class Params(CoreModel):
    search_util: SearchUtils = field(
        description="Type of the search utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="search_util", id="change_search_util")
async def change_search_util_type(metadata: MetaDataBase, *_: Any):
    search_util = metadata.params["search_util"].value
    metadata.params = {}
    match search_util:
        case SearchUtils.arxiv_api.value:
            return arxiv_api_node.get_metadata()
        case SearchUtils.bing_serpapi.value:
            return bing_serpapi_node.get_metadata()
        case SearchUtils.duckduckgo_search.value:
            return duckduckgo_search_node.get_metadata()
        case SearchUtils.duckduckgo_serpapi.value:
            return duckduckgo_serpapi_node.get_metadata()
        case SearchUtils.google_place.value:
            return google_place_node.get_metadata()
        case SearchUtils.wikipedia_api.value:
            return wikipedia_api_node.get_metadata()
        case SearchUtils.wikipedia_search.value:
            return wikipedia_search_node.get_metadata()
        case _:
            return metadata
