from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="duckduckgo_search",
    task="web_search",
    description="Search the web using DuckDuckGo.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/web/web_search/duckduckgo_search/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/web/web_search/duckduckgo_search",
)


@func.set_input
class Inputs(CoreModel):
    query: str = Field(..., description="The search query.")


@func.set_param
class Params(CoreModel):
    max_results: int = Field(..., description="Maximum number of search.")


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The concatenated titles and summaries.")
