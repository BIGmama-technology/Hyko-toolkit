from enum import Enum

from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


func = ToolkitNode(
    name="Wikipedia search",
    task="Web search",
    category=Category.FUNCTION,
    cost=5,
    description="Search wikipedia summaries.",
    icon="wikipedia",
)


@func.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Enter your query here"),
    )


@func.set_param
class Params(CoreModel):
    num_results: int = field(description="Number of search results to return.")
    language: SupportedLanguages = field(description="The search Language.")


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="The concatenated titles and summaries.")
