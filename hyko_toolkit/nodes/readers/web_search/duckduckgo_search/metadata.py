from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Duckduckgo search",
    cost=2,
    icon="duckduckgo",
    description="Search the web using DuckDuckGo.",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Enter your query here"),
    )


@node.set_param
class Params(CoreModel):
    max_results: int = field(description="Maximum number of search.")


@node.set_output
class Outputs(CoreModel):
    result: str = field(description="The concatenated titles and summaries.")
