from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


node = ToolkitNode(
    name="Wikipedia search",
    cost=2,
    description="Search wikipedia summaries.",
    icon="wikipedia",
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
    num_results: int = field(description="Number of search results to return.")
    language: SupportedLanguages = field(description="The search Language.")


@node.set_output
class Outputs(CoreModel):
    result: str = field(description="The concatenated titles and summaries.")
