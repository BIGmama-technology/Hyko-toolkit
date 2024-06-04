from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Duckduckgo search",
    task="Web search",
    category=Category.FUNCTION,
    cost=5,
    icon="duckduckgo",
    description="Search the web using DuckDuckGo.",
)


@func.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Enter your query here"),
    )


@func.set_param
class Params(CoreModel):
    max_results: int = field(description="Maximum number of search.")


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="The concatenated titles and summaries.")
