from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .arxiv_api.metadata import func as arxiv_api_node
from .bing_serpapi.metadata import func as bing_serpapi_node
from .duckduckgo_search.metadata import func as duckduckgo_search_node
from .duckduckgo_serpapi.metadata import func as duckduckgo_serpapi_node
from .google_place.metadata import func as google_place_node
from .google_search.metadata import func as google_search_node
from .wikipedia_api.metadata import func as wikipedia_api_node
from .wikipedia_search.metadata import func as wikipedia_search_node

node = NodeGroup(
    name="Web search",
    description="perform various search and retrieval tasks.",
    icon="stack",
    tag=Tag.readers,
    nodes=[
        arxiv_api_node,
        bing_serpapi_node,
        duckduckgo_search_node,
        duckduckgo_serpapi_node,
        google_place_node,
        wikipedia_api_node,
        wikipedia_search_node,
        google_search_node,
    ],
)
