from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


func = ToolkitFunction(
    name="wikipedia_search",
    task="web_search",
    description="Search wikipedia summaries.",
)


@func.set_input
class Inputs(CoreModel):
    query: str = Field(
        ...,
        description="The search query.",
    )


@func.set_param
class Params(CoreModel):
    num_results: int = Field(
        ...,
        description="Number of search results to return.",
    )
    language: SupportedLanguages = Field(
        ...,
        description="The search Language.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The concatenated titles and summaries.")
